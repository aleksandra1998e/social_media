from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import BaseModel
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    name = Column(String)
    posts = relationship("Post", back_populates="user")

    def check_password(self, password: str):
        return pwd_context.verify(password, self.password_hash)


class Post(BaseModel):
    __tablename__ = "posts"
    title = Column(String)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post")


class Like(BaseModel):
    __tablename__ = "likes"
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
