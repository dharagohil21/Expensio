from sqlalchemy import Column, Integer, String
from src.common.models import BaseModel

class User(BaseModel):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    name = Column(String(100), nullable=True)
