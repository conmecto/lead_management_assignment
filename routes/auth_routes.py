from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import AccountService
from schemas import KeyAccountManagerSignup, KeyAccountManagerLogin
from config.database import db_instance

router = APIRouter()

@router.post("/auth/signup")
def signup(kam_data: KeyAccountManagerSignup, db: Session = Depends(db_instance.get_db)):
    account_service = AccountService(db)
    kam = account_service.signup(kam_data)
    return kam

@router.post("/auth/login")
def login(kam_data: KeyAccountManagerLogin, db: Session = Depends(db_instance.get_db)):
    account_service = AccountService(db)
    login_response = account_service.login(kam_data)
    return login_response