from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate

async def create_client(
    db: AsyncSession, data: ClientCreate, tenant_id: UUID
) -> Client:
    client = Client(**data.model_dump(), tenant_id=tenant_id)
    db.add(client)
    await db.commit()
    await db.refresh(client)
    return client

async def get_clients(
    db: AsyncSession, tenant_id: UUID
) -> list[Client]:
    result = await db.execute(
        select(Client)
        .where(Client.tenant_id == tenant_id)
        .order_by(Client.created_at.desc())
    )
    return result.scalars().all()

async def get_client(
    db: AsyncSession, client_id: UUID, tenant_id: UUID
) -> Client:
    result = await db.execute(
        select(Client)
        .where(Client.id == client_id)
        .where(Client.tenant_id == tenant_id)
    )
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="العميل غير موجود")
    return client

async def update_client(
    db: AsyncSession, client_id: UUID, data: ClientUpdate, tenant_id: UUID
) -> Client:
    client = await get_client(db, client_id, tenant_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(client, key, value)
    await db.commit()
    await db.refresh(client)
    return client

async def delete_client(
    db: AsyncSession, client_id: UUID, tenant_id: UUID
) -> None:
    client = await get_client(db, client_id, tenant_id)
    await db.delete(client)
    await db.commit()