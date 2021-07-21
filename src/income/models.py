"""
Author: Nachiket Panchal
"""
from src.common.models import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.dialects.mysql import DATE
from src.users.models import User


class Income(BaseModel):
    __tablename__ = "income"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    title = Column(String(100), nullable=True)
    amount = Column(Float, nullable=False)
    income_category = Column(String(100), nullable=False)
    is_recurring = Column(Boolean, nullable=False, default=False)
    date = Column(DATE, nullable=False)