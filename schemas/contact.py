from pydantic import BaseModel
from utils.enums import ContactRole

class ContactCreate(BaseModel):
    name: str
    role: ContactRole
    email: str
    phone: str
    is_primary: bool

    class Config:
        orm_mode = True