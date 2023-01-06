from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer


class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)
