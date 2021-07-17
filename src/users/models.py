from app import db
from sqlalchemy import Column, Integer, String

class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    name = Column(String(100), nullable=True)
