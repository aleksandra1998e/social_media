import jwt
import os

from datetime import datetime, timedelta

from .auth import HTTPAuthorizationHeader
from ..db.models import User

from fastapi import Request, HTTPException
from sqlalchemy.orm import Session

JWT_SECRET_KEY = os.environ.get('DATABASE_URI')


def create_access_token(user_id: int):
    """Create JWT access token"""
    expiry = datetime.utcnow() + timedelta(minutes=30)
    payload = {"user_id": user_id, "exp": expiry}
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return token.decode(), expiry


def decode(token: str):
    """Decode JWT token"""
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])


def create_refresh_token(user_id: int):
    """Create JWT refresh token"""
    expiry = datetime.utcnow() + timedelta(days=7)
    payload = {"user_id": user_id, "exp": expiry}
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return token.decode(), expiry


def get_current_token(request: Request):
    """Get current JWT token"""
    auth_header = HTTPAuthorizationHeader(request.headers.get("Authorization"))
    return auth_header.credentials


def get_user_id(token: str, db: Session):
    """Get user ID from JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY)
        user_id = payload["user_id"]
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Not authenticated")

