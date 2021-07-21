"""
Author: Nachiket Panchal, Rushikesh Patel
"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, Schema
from src.income.models import Income, IncomeCategory
from datetime import date

class IncomeSchema(SQLAlchemyAutoSchema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(missing=date.today)
    user_id = fields.Integer(dump_only=True)

    class Meta:
        model = Income
        include_relationships = False
        include_fk = True
        load_instance = True


class IncomeListSchema(Schema):
    date = fields.Date(required=False, missing=date.today)


class IncomeCategorySchema(SQLAlchemyAutoSchema):
    id = fields.Integer(dump_only=True)

    class Meta:
        model = IncomeCategory
        include_relationships = False
        include_fk = True
        load_instance = True
