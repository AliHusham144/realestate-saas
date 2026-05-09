from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import decode_token
from app.models.tenant import Tenant
from jose import JWTError

bearer = HTTPBearer()

async def get_current_tenant(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db)
) -> Tenant:
    try:
        payload = decode_token(credentials.credentials)
        tenant_id = payload.get("sub")
        if not tenant_id:
            raise HTTPException(status_code=401, detail="Token غير صالح")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token منتهي أو غير صالح")

    result = await db.execute(select(Tenant).where(Tenant.id == tenant_id))
    tenant = result.scalar_one_or_none()

    if not tenant:
        raise HTTPException(status_code=401, detail="المستخدم غير موجود")

    return tenant