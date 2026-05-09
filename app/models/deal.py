import uuid
from enum import Enum
from sqlalchemy import String, Numeric, Text, ForeignKey, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.models.base import TimestampMixin
from datetime import date, datetime
from typing import Optional

class DealStage(str, Enum):
    initial = "initial"          # تواصل أولي
    viewing = "viewing"          # معاينة
    negotiating = "negotiating"  # مفاوضة
    contract = "contract"        # عقد
    closed = "closed"            # مغلقة
    cancelled = "cancelled"      # ملغاة

class Deal(Base, TimestampMixin):
    __tablename__ = "deals"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), index=True
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("clients.id"), index=True
    )
    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("properties.id"), index=True
    )
    stage: Mapped[DealStage] = mapped_column(default=DealStage.initial)
    deal_value: Mapped[float] = mapped_column(Numeric(12, 2))
    commission_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=2.5)
    commission_amt: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    expected_close: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)