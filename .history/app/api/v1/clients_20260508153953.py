from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.models.tenant import Tenant
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse
from app.services import client_service

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("", response_model=ClientResponse)
async def create(
    data: ClientCreate,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    return await client_service.create_client(db, data, tenant.id)

@router.get("", response_model=list[ClientResponse])
async def list_clients(
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    return await client_service.get_clients(db, tenant.id)

@router.get("/{client_id}", response_model=ClientResponse)
async def get_one(
    client_id: UUID,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    return await client_service.get_client(db, client_id, tenant.id)

@router.patch("/{client_id}", response_model=ClientResponse)
async def update(
    client_id: UUID,
    data: ClientUpdate,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    return await client_service.update_client(db, client_id, data, tenant.id)

@router.delete("/{client_id}")
async def delete(
    client_id: UUID,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    await client_service.delete_client(db, client_id, tenant.id)
    return {"message": "تم حذف العميل"}