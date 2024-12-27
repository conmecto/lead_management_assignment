from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from utils.enums import LeadStatus, LeadType
from .key_account_manager import KeyAccountManagerSchema

class LeadBase(BaseModel):
    name: str
    address: str
    city: str
    state: str
    status: Optional[LeadStatus] = LeadStatus.NEW

class LeadCreate(LeadBase):
    pass

class LeadSchema(LeadBase):
    id: int
    type: LeadType
    created_at: datetime
    deleted_at: Optional[datetime]
    kam_id: KeyAccountManagerSchema

    class Config:
        from_attributes = True