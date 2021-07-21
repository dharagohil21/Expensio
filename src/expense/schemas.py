from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, Schema
from src.expense.models import Expense
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