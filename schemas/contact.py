from pydantic import BaseModel, EmailStr
from utils.enums import ContactRole

class ContactCreate(BaseModel):
    name: str
    role: ContactRole
    email: EmailStr
    phone: str
    is_primary: bool

    class Config:
        from_attributes = True