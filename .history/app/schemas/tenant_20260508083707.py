from pydantic import BaseModel, EmailStr
from uuid import UUID

class TenantRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class TenantLogin(BaseModel):
    email: EmailStr
    password: str

class TenantResponse(BaseModel):
    id: UUID
    name: str
    email: str
    plan: str

    model_config = {"from_attributes": True}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"