"""
Author: Sravani Pinninti, Jaspreet Kaur Gill, Rushikesh Patel
"""
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from marshmallow import ValidationError
from flask import g
from flask_restful import Resource, request, current_app
from src.expense.schemas import ExpenseSchema, ExpenseListSchema, ExpenseCategorySchema
from src.expense.models import Expense, ExpenseCategory
from src.utils.helpers import get_response_obj
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from src.common.models import db
from src.auth.api import AuthResource


class ExpenseResource(AuthResource):

    def get(self, expense_id):
        expense = Expense.query.filter_by(id=expense_id).first()
        expense_schema = ExpenseSchema()
        if not expense:
            return get_response_obj("No expenses found", error="No expense with given id"), 404

        return (
            get_response_obj("expense data", data=expense_schema.dump(expense)),
            200,
        )

    def delete(self, expense_id):
        expense = Expense.query.get(expense_id)
        current_user = g.current_user
        if not expense:
            return get_response_obj("No expenses found", error="No expense with given id"), 404

        try:
            next_month_date = expense.date + relativedelta(months=1)
            next_month_start = date(next_month_date.year, next_month_date.month, 1)
            Expense.query.filter(
                and_(
                    Expense.user_id == current_user.id,
                    Expense.date >= next_month_start,
                    Expense.amount == expense.amount,
                    Expense.expense_category == expense.expense_category,
                    Expense.is_recurring == True,
                )
            ).delete()
            expense.delete()
        except SQLAlchemyError as e:
            current_app.logger.exception("Error deleting expense")
            return get_response_obj(
                "Server error while deleting expense",
                error="Database error",
            ), 500

        return get_response_obj("Expense deleted", data=None), 200

    def put(self, expense_id):
        expense = Expense.query.filter_by(id=expense_id).first()
        if not expense:
            return get_response_obj("No expenses found", error="No expense with given id"), 404

        expense_schema = ExpenseSchema()
        try:
            req_data = request.json
            new_expense = expense_schema.load(req_data, session=db.session, partial=True)
        except ValidationError as e:
            current_app.logger.exception("Cannot update expense, invalid request data")
            return get_response_obj(
                "Cannot update expense, invalid request data",
                error=e.messages,
            ), 422

        if "title" in req_data and new_expense.title != expense.title:
            expense.title = new_expense.title
        if "amount" in req_data and new_expense.amount != expense.amount:
            expense.amount = new_expense.amount

        try:
            current_user = g.current_user
            if "is_recurring" in req_data and new_expense.is_recurring != expense.is_recurring:
                expense.is_recurring = new_expense.is_recurring
                if new_expense.is_recurring is False:
                    # when recurring flag is changed from true to false
                    next_month_date = expense.date + relativedelta(months=1)
                    next_month_start = date(next_month_date.year, next_month_date.month, 1)
                    Expense.query.filter(
                        and_(
                            Expense.user_id == current_user.id,
                            Expense.date >= next_month_start,
                            Expense.amount == expense.amount,
                            Expense.expense_category == expense.expense_category,
                            Expense.is_recurring == True,
                        )
                    ).delete()
            expense.update()
        except SQLAlchemyError as e:
            current_app.logger.exception("Error updating expense")
            return get_response_obj(
                "Server error while updating expense",
                error="Database error"
            ), 500

        return get_response_obj("Expense updated", data=expense_schema.dump(expense)), 200


class ExpenseListResource(AuthResource):

    def post(self):
        expense_schema = ExpenseSchema()
        current_user = g.current_user
        try:
            expense = expense_schema.load(request.json or {}, session=db.session())
        except ValidationError as e:
            return get_response_obj(
                "Cannot create an expense entry. Invalid request data",
                error=e.messages,
            ), 422
        expense.user_id = current_user.id
        try:
            expense.add()
        except SQLAlchemyError as e:
            current_app.logger.exception("Error creating expense")
            return (
                get_response_obj(
                    "Error creating an expense entry, Server error",
                    error="Server error",
                ),
                500,
            )

        return (
            get_response_obj("Expense created", data=expense_schema.dump(expense)),
            200,
        )

    def get(self):
        current_user = g.current_user
        expense_schema = ExpenseSchema()
        try:
            req_args = ExpenseListSchema().load(request.args or {})
        except ValidationError as e:
            current_app.logger.exception("Invalid request params")
            return get_response_obj("Invalid request params", error=e.messages), 422

        # create two dates representing first and last date of requested month
        start_date = date(req_args["date"].year, req_args["date"].month, 1)
        next_month_date = start_date + relativedelta(months=1)
        end_date = date(next_month_date.year, next_month_date.month, 1)
        current_app.logger.info("Listing expense from %s to %s", start_date, end_date)

        current_month_expenses = (
            Expense.query.filter_by(user_id=current_user.id)
            .filter(
                and_(
                    Expense.date >= start_date,
                    Expense.date < end_date
                )
            )
            .all()
        )

        if start_date >= date.today(): # if future date
            prev_month_recurr_expenses = Expense.query.filter(
                and_(
                    Expense.date >= start_date + relativedelta(months=-1),
                    Expense.date < start_date,
                    Expense.is_recurring == True
                )
            ).all()
            new_expenses = list()
            for exp in prev_month_recurr_expenses:
                matched_expense = next(
                    (
                        e for e in current_month_expenses
                        if e.amount == exp.amount
                        and e.expense_category == exp.expense_category
                        and e.is_recurring is True
                    ),
                    None,
                )
                if matched_expense is not None:
                    current_app.logger.info("Recurring expense entry found")
                    continue

                expense = Expense(
                    user_id=current_user.id,
                    title=exp.title,
                    amount=exp.amount,
                    expense_category=exp.expense_category,
                    is_recurring=True,
                    date=start_date,
                )
                new_expenses.append(expense)
                current_app.logger.info("creating new recurring expense")
            try:
                session = db.session
                session.add_all(new_expenses)
                session.commit()
                current_month_expenses += new_expenses
            except SQLAlchemyError as e:
                current_app.logger.exception("Error creating recurring expense")
                return get_response_obj("Server error listing expense", error="Database error"), 500

        return (
            get_response_obj("expense list", data=expense_schema.dump(current_month_expenses, many=True)),
            200,
        )


class ExpenseCategoryListResource(AuthResource):

    def get(self):
        expense_categories = ExpenseCategory.query.all()
        schema = ExpenseCategorySchema()
        return get_response_obj("Expense categories", data=schema.dump(expense_categories, many=True))

    def post(self):
        schema = ExpenseCategorySchema()
        try:
            category = schema.load(request.json or {}, session=db.session)
        except ValidationError as e:
            return get_response_obj(
                "Cannot create an expense category. Invalid request data",
                error=e.messages,
            ), 422
        try:
            category.add()
        except SQLAlchemyError as e:
            current_app.logger.exception("Error creating expense category")
            return (
                get_response_obj(
                    "Error creating an expense category, Server error",
                    error="Server error",
                ),
                500,
            )

        return (
            get_response_obj("Expense category created", data=schema.dump(category)),
            200,
        )


class ExpenseCategoryResource(AuthResource):

    def delete(self, category_id):
        category = ExpenseCategory.query.get(category_id)
        if not category:
            return get_response_obj("No expenses category found", error="No category with given id"), 404

        try:
            category.delete()
        except SQLAlchemyError as e:
            current_app.logger.exception("Error deleting expense category")
            return get_response_obj(
                "Server error while deleting expense category",
                error="Database error",
            ), 500

        return get_response_obj("Expense deleted", data=None ), 200