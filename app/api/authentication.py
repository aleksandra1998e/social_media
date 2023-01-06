from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.schema import UserCreate, UserUpdate
from app.utils import jwt

router = APIRouter()


def get_db(request):
    return request.state.db


@router.post("/signup", response_model=UserCreate)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email is already taken
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT
    access_token = jwt.create_access_token(new_user.id)
    refresh_token = jwt.create_refresh_token(new_user.id)

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/login", response_model=UserUpdate)
def login(user: User, db: Session = Depends(get_db)):
    # Check if email and password are correct
    stored_user = db.query(User).filter(User.email == user.email).first()
    if not stored_user or not stored_user.check_password(user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Generate JWT
    access_token = jwt.create_access_token(stored_user.id)
    refresh_token = jwt.create_refresh_token(stored_user.id)

    return {"access_token": access_token, "refresh_token": refresh_token}
