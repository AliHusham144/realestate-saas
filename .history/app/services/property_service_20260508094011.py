from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.property import Property
from app.schemas.property import PropertyCreate, PropertyUpdate

async def create_property(
    db: AsyncSession, data: PropertyCreate, tenant_id: UUID
) -> Property:
    prop = Property(**data.model_dump(), tenant_id=tenant_id)
    db.add(prop)
    await db.commit()
    await db.refresh(prop)
    return prop

async def get_properties(
    db: AsyncSession, tenant_id: UUID
) -> list[Property]:
    result = await db.execute(
        select(Property)
        .where(Property.tenant_id == tenant_id)
        .where(Property.is_active == True)
        .order_by(Property.created_at.desc())
    )
    return result.scalars().all()

async def get_property(
    db: AsyncSession, property_id: UUID, tenant_id: UUID
) -> Property:
    result = await db.execute(
        select(Property)
        .where(Property.id == property_id)
        .where(Property.tenant_id == tenant_id)
    )
    prop = result.scalar_one_or_none()
    if not prop:
        raise HTTPException(status_code=404, detail="العقار غير موجود")
    return prop

async def update_property(
    db: AsyncSession, property_id: UUID, data: PropertyUpdate, tenant_id: UUID
) -> Property:
    prop = await get_property(db, property_id, tenant_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(prop, key, value)
    await db.commit()
    await db.refresh(prop)
    return prop

async def delete_property(
    db: AsyncSession, property_id: UUID, tenant_id: UUID
) -> None:
    prop = await get_property(db, property_id, tenant_id)
    prop.is_active = False
    await db.commit()