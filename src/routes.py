from flask import Blueprint
from flask_restful import Api
from src.users.views import UserResource, CreateUserResource
from src.expense.views import ExpenseResource, AddExpenseResource

# user api endpoints
user_bp = Blueprint("user_bp", __name__)
api = Api(user_bp)

api.add_resource(UserResource, "/<user_id>")
api.add_resource(CreateUserResource, "")

expense_bp = Blueprint("expense_bp",__name__)
api=Api(expense_bp)

api.add_resource(ExpenseResource,"/<user_id>")
api.add_resource(AddExpenseResource, "")