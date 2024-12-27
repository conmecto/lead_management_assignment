import jwt
import pytz
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Dict, Any
from utils.environments import AUTH_SECRET_KEY, AUTH_ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class AuthService:
    @staticmethod
    def issue_token(data: Dict[str, Any], expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(pytz.UTC) + expires_delta
        else:
            expire = datetime.now(pytz.UTC) + timedelta(minutes=60)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, AUTH_SECRET_KEY, algorithm=AUTH_ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
        if not token or token == "<your_token>":
            raise HTTPException(401, 'Unauthorized')
        payload = None
        try:
            payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, 'Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(498, 'Invalid token')
        if not payload or "kam_id" not in payload:
            raise HTTPException(401, 'Unauthorized')
        return payload
            