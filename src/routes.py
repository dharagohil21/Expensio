from flask import Blueprint
from flask_restful import Api
from src.users.views import UserResource, CreateUserResource, LoginResource
from src.expense.views import ExpenseResource, ExpenseListResource
from src.income.views import IncomeResource, IncomeListResource

# user api endpoints
user_bp = Blueprint("user_bp", __name__)
api = Api(user_bp)

api.add_resource(UserResource, "/<user_id>")
api.add_resource(CreateUserResource, "")
api.add_resource(LoginResource, "/login")

expense_bp = Blueprint("expense_bp",__name__)
api=Api(expense_bp)

api.add_resource(ExpenseResource,"/<expense_id>")
api.add_resource(ExpenseListResource, "")

income_bp = Blueprint("income_bp",__name__)
income_api=Api(income_bp)

income_api.add_resource(IncomeResource,"/<income_id>")
income_api.add_resource(IncomeListResource, "")
