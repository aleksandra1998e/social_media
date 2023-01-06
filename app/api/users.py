from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.schema import UserCreate, UserUpdate, UserOut
from app.utils import jwt
from app.utils.password import hash_password, check_password


router = APIRouter()


def get_db(request):
    return request.state.db


def get_current_user(request: Request, db: Session = Depends(get_db)):
    """Get current user from request"""
    user_id = request.headers.get("User-ID")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user with same email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already exists")

    # Hash password
    hashed_password = hash_password(user.password)

    # Create new user
    new_user = User(email=user.email, password_hash=hashed_password, name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate access and refresh tokens
    access_token = jwt.create_access_token(new_user.id)
    refresh_token = jwt.create_refresh_token(new_user.id)

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/users/login", response_model=UserOut)
def login(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user with email exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Check if password is correct
    if not check_password(user.password, existing_user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Generate access and refresh tokens
    access_token = jwt.create_access_token(existing_user.id)
    refresh_token = jwt.create_refresh_token(existing_user.id)

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/users/refresh", response_model=UserOut)
def refresh(db: Session = Depends(get_db), token: str = Depends(jwt.get_current_token)):
    # Get user from token
    user_id = jwt.get_user_id(token, db)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Token is invalid")

    # Generate new access and refresh tokens
    access_token = jwt.create_access_token(user.id)
    refresh_token = jwt.create_refresh_token(user.id)

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.put("/users/me", response_model=UserOut)
def update_user(user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Update user
    current_user.email = user.email or current_user.email
    current_user.password_hash = hash_password(user.password) if user.password else current_user.password_hash
    current_user.name = user.name or current_user.name
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    # Generate new access and refresh tokens
    access_token = jwt.create_access_token(current_user.id)
    refresh_token = jwt.create_refresh_token(current_user.id)

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get("/users/me", response_model=UserOut)
def read_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/users/verify", response_model=UserOut)
def verify_user(db: Session = Depends(get_db), token: str = Depends(jwt.get_current_token)):
    # Get user from token
    user_id = jwt.get_user_id(token, db)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Token is invalid")

    # Verify user
    user.verified = True
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate new access and refresh tokens
    access_token = jwt.create_access_token(user.id)
    refresh_token = jwt.create_refresh_token(user.id)

    return {"access_token": access_token, "refresh_token": refresh_token}
