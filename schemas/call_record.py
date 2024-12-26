from pydantic import BaseModel
from typing import Optional

class CallRecordCreate(BaseModel):
    kam_id: int
    lead_id: int
    contact_id: int

    class Config:
        orm_mode = True

class EndCallRecord(BaseModel):
    is_order_placed: bool
    order_value: Optional[int]
    is_lead_lost: Optional[bool]

    class Config:
        orm_mode = True