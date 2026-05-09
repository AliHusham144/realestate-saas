import uuid
from enum import Enum
from sqlalchemy import String, Numeric, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.models.base import TimestampMixin

class ClientStatus(str, Enum):
    new = "new"
    contacted = "contacted"
    viewing = "viewing"
    negotiating = "negotiating"
    closed = "closed"

class InterestType(str, Enum):
    apartment = "apartment"
    villa = "villa"
    land = "land"
    commercial = "commercial"
    any = "any"

class Client(Base, TimestampMixin):
    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), index=True
    )
    full_name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(20), index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    budget: Mapped[float] = mapped_column(Numeric(12, 2), nullable=True)
    interest_type: Mapped[InterestType] = mapped_column(default=InterestType.any)
    status: Mapped[ClientStatus] = mapped_column(default=ClientStatus.new)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)