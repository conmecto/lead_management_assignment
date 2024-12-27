from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import KeyAccountManager
from schemas import KeyAccountManagerLogin, KeyAccountManagerSignup
from repositories import KeyAccountManagerRepository
from .auth import AuthService
from utils.helpers import hash_password, verify_password

class AccountService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.kam_repo = KeyAccountManagerRepository(db_session)

    def signup(self, kam_data: KeyAccountManagerSignup) -> KeyAccountManager:
        
        kam_data_dict = kam_data.model_dump()
        hashed_password = hash_password(kam_data_dict["password"])
        kam_data_dict["password"] = hashed_password
        kam_id = self.kam_repo.create(kam_data_dict)
        if not kam_id:
            raise HTTPException(409, "Email already exists")
        return {"kam_id": kam_id}

    def login(self, kam_data: KeyAccountManagerLogin) -> str:
        kam_data_dict = kam_data.model_dump()
        kam = self.kam_repo.get_by_email(kam_data_dict["email"])
        if not kam or not verify_password(kam_data_dict["password"], kam.password):
            raise HTTPException(401, "Invalid credentials")
        token_data = {"sub": kam.email, "kam_id": kam.id}
        token = AuthService.issue_token(token_data)
        return {
            "kam_id": kam.id, 
            "access_token": token
        }