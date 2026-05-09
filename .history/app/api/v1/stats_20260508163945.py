from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.models.tenant import Tenant
from app.models.property import Property, PropertyStatus
from app.models.client import Client, ClientStatus
from app.models.deal import Deal, DealStage
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/stats", tags=["Dashboard"])

class DashboardStats(BaseModel):
    # العقارات
    total_properties: int
    available_properties: int
    reserved_properties: int
    sold_properties: int

    # العملاء
    total_clients: int
    new_clients: int
    active_clients: int

    # الصفقات
    total_deals: int
    open_deals: int
    closed_deals: int
    cancelled_deals: int

    # المالية
    total_commission: float
    total_deals_value: float
    avg_deal_value: float

@router.get("", response_model=DashboardStats)
async def get_stats(
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)
):
    tid = tenant.id

    # --- العقارات ---
    total_props = await db.scalar(
        select(func.count()).where(Property.tenant_id == tid)
    )
    available_props = await db.scalar(
        select(func.count()).where(
            and_(Property.tenant_id == tid, Property.status == PropertyStatus.available)
        )
    )
    reserved_props = await db.scalar(
        select(func.count()).where(
            and_(Property.tenant_id == tid, Property.status == PropertyStatus.reserved)
        )
    )
    sold_props = await db.scalar(
        select(func.count()).where(
            and_(Property.tenant_id == tid, Property.status == PropertyStatus.sold)
        )
    )

    # --- العملاء ---
    total_clients = await db.scalar(
        select(func.count()).where(Client.tenant_id == tid)
    )
    new_clients = await db.scalar(
        select(func.count()).where(
            and_(Client.tenant_id == tid, Client.status == ClientStatus.new)
        )
    )
    active_clients = await db.scalar(
        select(func.count()).where(
            and_(
                Client.tenant_id == tid,
                Client.status.in_([
                    ClientStatus.contacted,
                    ClientStatus.viewing,
                    ClientStatus.negotiating
                ])
            )
        )
    )

    # --- الصفقات ---
    total_deals = await db.scalar(
        select(func.count()).where(Deal.tenant_id == tid)
    )
    open_deals = await db.scalar(
        select(func.count()).where(
            and_(
                Deal.tenant_id == tid,
                Deal.stage.in_([
                    DealStage.initial,
                    DealStage.viewing,
                    DealStage.negotiating,
                    DealStage.contract
                ])
            )
        )
    )
    closed_deals = await db.scalar(
        select(func.count()).where(
            and_(Deal.tenant_id == tid, Deal.stage == DealStage.closed)
        )
    )
    cancelled_deals = await db.scalar(
        select(func.count()).where(
            and_(Deal.tenant_id == tid, Deal.stage == DealStage.cancelled)
        )
    )

    # --- المالية ---
    total_commission = await db.scalar(
        select(func.sum(Deal.commission_amt)).where(
            and_(Deal.tenant_id == tid, Deal.stage == DealStage.closed)
        )
    )
    total_deals_value = await db.scalar(
        select(func.sum(Deal.deal_value)).where(
            and_(Deal.tenant_id == tid, Deal.stage == DealStage.closed)
        )
    )
    avg_deal_value = await db.scalar(
        select(func.avg(Deal.deal_value)).where(Deal.tenant_id == tid)
    )

    return DashboardStats(
        total_properties=total_props or 0,
        available_properties=available_props or 0,
        reserved_properties=reserved_props or 0,
        sold_properties=sold_props or 0,
        total_clients=total_clients or 0,
        new_clients=new_clients or 0,
        active_clients=active_clients or 0,
        total_deals=total_deals or 0,
        open_deals=open_deals or 0,
        closed_deals=closed_deals or 0,
        cancelled_deals=cancelled_deals or 0,
        total_commission=float(total_commission or 0),
        total_deals_value=float(total_deals_value or 0),
        avg_deal_value=float(avg_deal_value or 0),
    )