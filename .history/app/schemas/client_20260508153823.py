from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from app.models.client import ClientStatus, InterestType

class ClientCreate(BaseModel):
    full_name: str
    phone: str
    email: Optional[str] = None
    budget: Optional[float] = None
    interest_type: InterestType = InterestType.any
    city: Optional[str] = None
    notes: Optional[str] = None

class ClientUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    budget: Optional[float] = None
    interest_type: Optional[InterestType] = None
    status: Optional[ClientStatus] = None
    city: Optional[str] = None
    notes: Optional[str] = None

class ClientResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    full_name: str
    phone: str
    email: Optional[str] = None
    budget: Optional[float] = None
    interest_type: InterestType
    status: ClientStatus
    city: Optional[str] = None
    notes: Optional[str] = None

    model_config = {"from_attributes": True}