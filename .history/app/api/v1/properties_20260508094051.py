from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.models.tenant import Tenant
from app.schemas.property import PropertyCreate, PropertyUpdate, PropertyResponse
from app.services import property_service

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.post("", response_model=PropertyResponse)
async def create(
    data: PropertyCreate,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    return await property_service.create_property(db, data, tenant.id)

@router.get("", response_model=list[PropertyResponse])
async def list_properties(
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    return await property_service.get_properties(db, tenant.id)

@router.get("/{property_id}", response_model=PropertyResponse)
async def get_one(
    property_id: UUID,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    return await property_service.get_property(db, property_id, tenant.id)

@router.patch("/{property_id}", response_model=PropertyResponse)
async def update(
    property_id: UUID,
    data: PropertyUpdate,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    return await property_service.update_property(db, property_id, data, tenant.id)

@router.delete("/{property_id}")
async def delete(
    property_id: UUID,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    await property_service.delete_property(db, property_id, tenant.id)
    return {"message": "تم حذف العقار"}