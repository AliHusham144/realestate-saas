from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from app.models.property import PropertyType, PropertyStatus

class PropertyCreate(BaseModel):
    title: str
    type: PropertyType = PropertyType.apartment
    price: float
    area_sqm: float
    bedrooms: int = 0
    bathrooms: int = 0
    city: str
    district: Optional[str] = None
    description: Optional[str] = None

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[PropertyType] = None
    status: Optional[PropertyStatus] = None
    price: Optional[float] = None
    area_sqm: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    city: Optional[str] = None
    district: Optional[str] = None
    description: Optional[str] = None

class PropertyResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    title: str
    type: PropertyType
    status: PropertyStatus
    price: float
    area_sqm: float
    bedrooms: int
    bathrooms: int
    city: str
    district: Optional[str] = None
    description: Optional[str] = None

    model_config = {"from_attributes": True}