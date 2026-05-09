from pydantic import BaseModel, model_validator
from uuid import UUID
from typing import Optional
from datetime import date, datetime
from app.models.deal import DealStage

class DealCreate(BaseModel):
    client_id: UUID
    property_id: UUID
    deal_value: float
    commission_pct: float = 2.5
    expected_close: Optional[date] = None
    notes: Optional[str] = None


class DealUpdate(BaseModel):
    stage: Optional[DealStage] = None
    deal_value: Optional[float] = None
    commission_pct: Optional[float] = None
    expected_close: Optional[date] = None
    notes: Optional[str] = None

class DealResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    client_id: UUID
    property_id: UUID
    stage: DealStage
    deal_value: float
    commission_pct: float
    commission_amt: float
    expected_close: Optional[date] = None
    closed_at: Optional[datetime] = None
    notes: Optional[str] = None

    model_config = {"from_attributes": True}