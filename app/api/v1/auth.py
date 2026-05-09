from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.schemas.tenant import TenantRegister, TenantLogin, TenantResponse, TokenResponse
from app.services.tenant_service import register_tenant, login_tenant
from app.models.tenant import Tenant

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TenantResponse)
async def register(data: TenantRegister, db: AsyncSession = Depends(get_db)):
    return await register_tenant(db, data)

@router.post("/login", response_model=TokenResponse)
async def login(data: TenantLogin, db: AsyncSession = Depends(get_db)):
    token = await login_tenant(db, data.email, data.password)
    return {"access_token": token}

@router.get("/me", response_model=TenantResponse)
async def me(current_tenant: Tenant = Depends(get_current_tenant)):
    return current_tenant