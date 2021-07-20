from app import db
from sqlalchemy import Column, Integer, String

class Expense(db.Model):
    __tablename__ = "expense"

    expense_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    amount = Column(String(100), nullable=False)
    expense_category = Column(String(100), nullable=False)
    recurring = Column(String(100), nullable=True)
    date = Column(String(100), nullable=True)
