"""
Author: Rushikesh Patel, Sravani Pinninti, Jaspreet Kaur Gill, Nachiket Panchal, Dharaben Gohil
"""
from flask import Blueprint
from flask_restful import Api
from src.users.views import UserResource, CreateUserResource, LoginResource
from src.expense.views import (
    ExpenseResource,
    ExpenseListResource,
    ExpenseCategoryResource,
    ExpenseCategoryListResource,
    ExpenseCategoryLimitResource,
    ExpenseCategoryLimitListResource,
)
from src.income.views import (
    IncomeResource,
    IncomeListResource,
    IncomeCategoryResource,
    IncomeCategoryListResource,
)

from src.stats.views import DashBoardApi, StatGraphApi

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
expense_api.add_resource(ExpenseCategoryLimitListResource, "/category/limit")
expense_api.add_resource(ExpenseCategoryLimitResource, "/category/limit/<limit_id>")

# income api endpoints
income_bp = Blueprint("income_bp",__name__)
income_api = Api(income_bp)
income_api.add_resource(IncomeResource,"/<income_id>")
income_api.add_resource(IncomeListResource, "")
income_api.add_resource(IncomeCategoryListResource, "/category")
income_api.add_resource(IncomeCategoryResource, "/category/<category_id>")

# stats endpoints
stats_bp = Blueprint("stats_bp", __name__)
stats_api = Api(stats_bp)
stats_api.add_resource(DashBoardApi, "/dashboard")
stats_api.add_resource(StatGraphApi, "/graph")
