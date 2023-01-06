from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    name: str


class UserUpdate(BaseModel):
    email: str = None
    password: str = None
    name: str = None


class UserOut(BaseModel):
    access_token: str
    refresh_token: str


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: str = None
    content: str = None


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
