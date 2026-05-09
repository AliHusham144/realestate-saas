from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tenant import Tenant
from app.schemas.tenant import TenantRegister
from app.core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status

async def register_tenant(db: AsyncSession, data: TenantRegister) -> Tenant:
    # تحقق أن الإيميل غير مستخدم
    result = await db.execute(select(Tenant).where(Tenant.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="الإيميل مستخدم مسبقاً"
        )
    tenant = Tenant(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    db.add(tenant)
    await db.commit()
    await db.refresh(tenant)
    return tenant

async def login_tenant(db: AsyncSession, email: str, password: str) -> str:
    result = await db.execute(select(Tenant).where(Tenant.email == email))
    tenant = result.scalar_one_or_none()

    if not tenant or not verify_password(password, tenant.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="إيميل أو كلمة مرور غلط"
        )

    token = create_access_token({"sub": str(tenant.id)})
    return token