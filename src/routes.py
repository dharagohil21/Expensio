from flask import Blueprint
from flask_restful import Api
from src.users.views import UserResource, CreateUserResource, LoginResource
from src.expense.views import (
    ExpenseResource,
    ExpenseListResource,
    ExpenseCategoryResource,
    ExpenseCategoryListResource,
)
from src.income.views import (
    IncomeResource,
    IncomeListResource,
    IncomeCategoryResource,
    IncomeCategoryListResource,
)

# user api endpoints
user_bp = Blueprint("user_bp", __name__)
user_api = Api(user_bp)
user_api.add_resource(UserResource, "/<user_id>")
user_api.add_resource(CreateUserResource, "")
user_api.add_resource(LoginResource, "/login")

# expense api endpoints
expense_bp = Blueprint("expense_bp",__name__)
expense_api = Api(expense_bp)
expense_api.add_resource(ExpenseResource,"/<expense_id>")
expense_api.add_resource(ExpenseListResource, "")
expense_api.add_resource(ExpenseCategoryListResource, "/category")
expense_api.add_resource(ExpenseCategoryResource, "/category/<category_id>")

# income api endpoints
income_bp = Blueprint("income_bp",__name__)
income_api=Api(income_bp)
income_api.add_resource(IncomeResource,"/<income_id>")
income_api.add_resource(IncomeListResource, "")
income_api.add_resource(IncomeCategoryListResource, "/category")
income_api.add_resource(IncomeCategoryResource, "/category/<category_id>")
