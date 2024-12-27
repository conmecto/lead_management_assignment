from pydantic import BaseModel
from typing import Optional

class CallRecordCreate(BaseModel):
    contact_id: int

    class Config:
        from_attributes = True

class EndCallRecord(BaseModel):
    is_order_placed: Optional[bool] = False 
    order_value: Optional[int] = None
    is_lead_lost: Optional[bool] = None

    class Config:
        from_attributes = True