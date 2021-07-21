"""
Author: Sravani Pinninti
"""
from src.common.models import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.dialects.mysql import DATE
from src.users.models import User


class Expense(BaseModel):
    __tablename__ = "expense"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    title = Column(String(100), nullable=True)
    amount = Column(Float, nullable=False)
    expense_category = Column(String(100), nullable=False)
    is_recurring = Column(Boolean, nullable=True, default=False)
    date = Column(DATE, nullable=False)


class ExpenseCategory(BaseModel):
    __tablename__ = "expense_category"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
