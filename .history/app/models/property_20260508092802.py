import uuid
from enum import Enum
from sqlalchemy import String, Numeric, Integer, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class PropertyType(str, Enum):
    apartment = "apartment"
    villa = "villa"
    land = "land"
    commercial = "commercial"

class PropertyStatus(str, Enum):
    available = "available"
    reserved = "reserved"
    sold = "sold"

class Property(Base, TimestampMixin):
    __tablename__ = "properties"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), index=True
    )
    title: Mapped[str] = mapped_column(String(255))
    type: Mapped[PropertyType] = mapped_column(default=PropertyType.apartment)
    status: Mapped[PropertyStatus] = mapped_column(default=PropertyStatus.available)
    price: Mapped[float] = mapped_column(Numeric(12, 2))
    area_sqm: Mapped[float] = mapped_column(Numeric(8, 2))
    bedrooms: Mapped[int] = mapped_column(Integer, default=0)
    bathrooms: Mapped[int] = mapped_column(Integer, default=0)
    city: Mapped[str] = mapped_column(String(100))
    district: Mapped[str] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    tenant: Mapped["Tenant"] = relationship(back_populates="properties")