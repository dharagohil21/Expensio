from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.expense.models import Expense

class ExpenseSchema(SQLAlchemyAutoSchema):
    expense_id = fields.Integer(dump_only=True) # read-only by user request

    class Meta:
        model = Expense
        include_relationships = False
        include_fk = True
        load_instance = True