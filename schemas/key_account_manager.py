from pydantic import BaseModel, EmailStr
from datetime import datetime

class KeyAccountManagerLogin(BaseModel):
    email: EmailStr
    password: str

class KeyAccountManagerSignup(KeyAccountManagerLogin):
    name: str

class KeyAccountManagerSchema(KeyAccountManagerSignup):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

