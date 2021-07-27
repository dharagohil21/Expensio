from datetime import date
from sqlalchemy import and_
from flask import g, current_app
from dateutil.relativedelta import relativedelta
from src.auth.api import AuthResource
from src.utils.helpers import get_response_obj
from src.expense.models import ExpenseCategoryLimit, Expense
from src.expense.schemas import ExpenseSchema
from src.income.schemas import IncomeSchema
from src.income.models import Income


class DashBoardApi(AuthResource):

    def calc_expense_limit_sum(self):
        current_user = g.current_user
        expense_limits = ExpenseCategoryLimit.query.filter_by(
            user_id=current_user.id
        )
        total = sum(limit.amount for limit in expense_limits)
        return total

    def calc_expense_total(self, start_date, end_date):
        current_user = g.current_user

        expenses = Expense.query.filter(
            and_(
                Expense.user_id==current_user.id,
                Expense.date>=start_date,
                Expense.date<end_date
            )
        ).all()
        total = sum(exp.amount for exp in expenses)
        return total

    def calc_total_income(self, start_date, end_date):
        current_user = g.current_user

        incomes = Income.query.filter(
            and_(
                Expense.user_id==current_user.id,
                Expense.date>=start_date,
                Expense.date<end_date
            )
        ).all()
        total = sum(inc.amount for inc in incomes)
        return total

    def get_recurring_expense(self, start_date, end_date):
        current_user = g.current_user

        expenses = Expense.query.filter(
            and_(
                Expense.is_recurring==True,
                Expense.user_id==current_user.id,
                Expense.date>=start_date,
                Expense.date<end_date,
            )
        ).all()
        return expenses

    def get_recurring_income(self, start_date, end_date):
        current_user = g.current_user

        incomes = Income.query.filter(
            and_(
                Income.is_recurring==True,
                Income.user_id==current_user.id,
                Income.date>=start_date,
                Income.date<end_date,
            )
        ).all()
        return incomes

    def get(self):
        resp_data = dict()
        today = date.today()
        start_date = date(today.year, today.month, 1)
        next_month_date = start_date + relativedelta(months=1)
        end_date = date(next_month_date.year, next_month_date.month, 1)

        resp_data["total_expense_limit"] = self.calc_expense_limit_sum()

        total_expense = self.calc_expense_total(start_date, end_date)
        resp_data["remaining_expense_limit"] = (
            abs(resp_data["total_expense_limit"] - total_expense)
        )

        resp_data["total_income"] = self.calc_total_income(start_date, end_date)
        resp_data["remaining_income"] = resp_data["total_income"] - total_expense

        recurring_expenses = self.get_recurring_expense(start_date, end_date)
        resp_data["recurring_expenses"] = ExpenseSchema(only=("title", "amount", "id")).dump(
            recurring_expenses, many=True,
        )

        recurring_incomes = self.get_recurring_income(start_date, end_date)
        resp_data["recurring_incomes"] = IncomeSchema(only=("title", "amount", "id")).dump(
            recurring_incomes, many=True
        )

        return get_response_obj("Dashboard data", data=resp_data), 200
