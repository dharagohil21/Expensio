"""
Author: Sravani Pinninti
"""
from datetime import date, timedelta
from dateutil.rrule import rrule, MONTHLY
from marshmallow import ValidationError
from flask import g
from flask_restful import Resource, request, current_app
from src.expense.schemas import ExpenseSchema, ExpenseListSchema
from src.expense.models import Expense
from src.utils.helpers import get_response_obj
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from src.common.models import db
from src.auth.api import AuthResource


class ExpenseResource(Resource):

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

        if not expense:
            return get_response_obj("No expenses found", error="No expense with given id"), 404

        try:
            expense.delete()
        except SQLAlchemyError as e:
            current_app.logger.exception("Error deleting expense")
            return get_response_obj(
                "Server error while deleting expense",
                error="Database error",
            ), 500

        return get_response_obj("Expense deleted", data=None), 200


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

        start_date = date(req_args["date"].year, req_args["date"].month, 1)
        next_month_date = rrule(freq=MONTHLY, count=2, dtstart=start_date)[1]
        end_date = date(next_month_date.year, next_month_date.month, 1)
        current_app.logger.info("Listing expense from %s to %s", start_date, end_date)

        expenses = (
            Expense.query.filter_by(user_id=current_user.id)
            .filter(
                and_(
                    Expense.date >= start_date,
                    Expense.date < end_date
                )
            )
            .all()
        )
        return (
            get_response_obj("expense list", data=expense_schema.dump(expenses, many=True)),
            200,
        )
