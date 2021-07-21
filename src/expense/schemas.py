"""
Author: Sravani Pinninti, Rushikesh Patel, Dharaben Gohil
"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, Schema
from src.expense.models import Expense, ExpenseCategory, ExpenseCategoryLimit
from datetime import date


class ExpenseSchema(SQLAlchemyAutoSchema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(missing=date.today)
    user_id = fields.Integer(dump_only=True)

    class Meta:
        model = Expense
        include_relationships = False
        include_fk = True
        load_instance = True


class ExpenseListSchema(Schema):
    date = fields.Date(required=False, missing=date.today)


class ExpenseCategorySchema(SQLAlchemyAutoSchema):
    id = fields.Integer(dump_only=True)

    class Meta:
        model = ExpenseCategory
        include_relationships = False
        include_fk = True
        load_instance = True


class ExpenseCategoryLimitSchema(SQLAlchemyAutoSchema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)

    class Meta:
        model = ExpenseCategoryLimit
        include_relationships = False
        include_fk = True
        load_instance = True
