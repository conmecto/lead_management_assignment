from pydantic import BaseModel
from datetime import datetime

class KeyAccountManagerBase(BaseModel):
    name: str
    email: str
    phone: str

class KeyAccountManagerSchema(KeyAccountManagerBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True