from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.models.tenant import Tenant
from app.schemas.deal import DealCreate, DealUpdate, DealResponse
from app.services import deal_service

router = APIRouter(prefix="/deals", tags=["Deals"])

@router.post("", response_model=DealResponse)
async def create(
    data: DealCreate,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    return await deal_service.create_deal(db, data, tenant.id)

@router.get("", response_model=list[DealResponse])
async def list_deals(
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    return await deal_service.get_deals(db, tenant.id)

@router.get("/{deal_id}", response_model=DealResponse)
async def get_one(
    deal_id: UUID,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    return await deal_service.get_deal(db, deal_id, tenant.id)

@router.patch("/{deal_id}", response_model=DealResponse)
async def update(
    deal_id: UUID,
    data: DealUpdate,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    return await deal_service.update_deal(db, deal_id, data, tenant.id)