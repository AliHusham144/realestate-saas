from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.deal import Deal, DealStage
from app.models.property import Property, PropertyStatus
from app.schemas.deal import DealCreate, DealUpdate

async def create_deal(
    db: AsyncSession, data: DealCreate, tenant_id: UUID
) -> Deal:
    # تحقق أن العقار متاح
    result = await db.execute(
        select(Property)
        .where(Property.id == data.property_id)
        .where(Property.tenant_id == tenant_id)
    )
    prop = result.scalar_one_or_none()
    if not prop:
        raise HTTPException(status_code=404, detail="العقار غير موجود")
    if prop.status == PropertyStatus.sold:
        raise HTTPException(status_code=400, detail="العقار مباع مسبقاً")

    commission_amt = data.deal_value * data.commission_pct / 100
    deal = Deal(
        **data.model_dump(),
        tenant_id=tenant_id,
        commission_amt=commission_amt
    )
    db.add(deal)

    # غيّر حالة العقار لـ reserved
    prop.status = PropertyStatus.reserved
    await db.commit()
    await db.refresh(deal)
    return deal

async def get_deals(
    db: AsyncSession, tenant_id: UUID
) -> list[Deal]:
    result = await db.execute(
        select(Deal)
        .where(Deal.tenant_id == tenant_id)
        .order_by(Deal.created_at.desc())
    )
    return result.scalars().all()

async def get_deal(
    db: AsyncSession, deal_id: UUID, tenant_id: UUID
) -> Deal:
    result = await db.execute(
        select(Deal)
        .where(Deal.id == deal_id)
        .where(Deal.tenant_id == tenant_id)
    )
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="الصفقة غير موجودة")
    return deal

async def update_deal(
    db: AsyncSession, deal_id: UUID, data: DealUpdate, tenant_id: UUID
) -> Deal:
    deal = await get_deal(db, deal_id, tenant_id)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(deal, key, value)

    # إذا أُغلقت الصفقة — غيّر حالة العقار لـ sold
    if data.stage == DealStage.closed:
        deal.closed_at = datetime.utcnow()
        result = await db.execute(
            select(Property).where(Property.id == deal.property_id)
        )
        prop = result.scalar_one_or_none()
        if prop:
            prop.status = PropertyStatus.sold

    # إذا أُلغيت — أعد العقار لـ available
    if data.stage == DealStage.cancelled:
        result = await db.execute(
            select(Property).where(Property.id == deal.property_id)
        )
        prop = result.scalar_one_or_none()
        if prop:
            prop.status = PropertyStatus.available

    if data.deal_value or data.commission_pct:
        deal.commission_amt = deal.deal_value * deal.commission_pct / 100

    await db.commit()
    await db.refresh(deal)
    return deal