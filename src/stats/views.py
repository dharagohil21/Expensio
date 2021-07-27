from datetime import date, timedelta
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


class StatGraphApi(AuthResource):

    def get_expenses(self, start_date, end_date):
        current_user = g.current_user
        expenses = Expense.query.filter(
            Expense.user_id == current_user.id,
            Expense.date >= start_date,
            Expense.date < end_date,
        ).order_by(Expense.date).all()
        return expenses

    def get_incomes(self, start_date, end_date):
        current_user = g.current_user
        expenses = Income.query.filter(
            Income.user_id == current_user.id,
            Income.date >= start_date,
            Income.date < end_date,
        ).order_by(Income.date).all()
        return expenses

    def calc_week_total(self, input_list):
        total = {
            "0": 0,
            "8": 0,
            "15": 0,
            "22": 0,
        }

        for i in range(len(input_list)):
            if input_list[i].date.day<8:
                total["0"] += input_list[i].amount
            elif input_list[i].date.day<15:
                total["8"] += input_list[i].amount
            elif input_list[i].date.day<22:
                total["15"] += input_list[i].amount
            else:
                total["22"] += input_list[i].amount

        return total

    def get(self):
        resp_data = dict()
        today = date.today()
        current_month_start = date(today.year, today.month, 1)
        next_month_date = current_month_start + relativedelta(months=1)
        current_month_end = date(next_month_date.year, next_month_date.month, 1)

        prev_month_start = current_month_start + relativedelta(months=-1)
        prev_month_end = current_month_end + relativedelta(months=-1)

        # expense graph
        current_month_expense = self.get_expenses(current_month_start, current_month_end)
        prev_month_expense = self.get_expenses(prev_month_start, prev_month_end)
        current_month_expense_stat = self.calc_week_total(current_month_expense)
        prev_month_expense_stat = self.calc_week_total(prev_month_expense)

        # income graph
        current_month_incomes = self.get_incomes(current_month_start, current_month_end)
        prev_month_incomes = self.get_incomes(prev_month_start, prev_month_end)
        current_month_income_stat = self.calc_week_total(current_month_incomes)
        prev_month_income_stat = self.calc_week_total(prev_month_incomes)

        resp_data["current_month_expense"] = [
            current_month_expense_stat["0"], current_month_expense_stat["8"],
            current_month_expense_stat["15"], current_month_expense_stat["22"],
        ]
        resp_data["prev_month_expense"] = [
            prev_month_expense_stat["0"], prev_month_expense_stat["8"],
            prev_month_expense_stat["15"], prev_month_expense_stat["22"],
        ]
        resp_data["current_month_expense"] = [
            current_month_income_stat["0"], current_month_income_stat["8"],
            current_month_income_stat["15"], current_month_income_stat["22"],
        ]
        resp_data["prev_month_expense"] = [
            prev_month_income_stat["0"], prev_month_income_stat["8"],
            prev_month_income_stat["15"], prev_month_income_stat["22"],
        ]

        expense_by_category = dict()
        for exp in current_month_expense:
            sum = expense_by_category.setdefault(exp.expense_category,0)
            expense_by_category[exp.expense_category]+=exp.amount
        resp_data["expense_by_category"] = expense_by_category

        income_by_category = dict()
        for inc in current_month_incomes:
            sum = income_by_category.setdefault(inc.income_category,0)
            income_by_category[inc.income_category]+=inc.amount
        resp_data["income_by_category"] = income_by_category

        return get_response_obj("Graph data", data=resp_data), 200
