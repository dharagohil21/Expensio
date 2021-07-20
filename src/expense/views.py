from marshmallow import ValidationError
from flask import g
from flask_restful import Resource, request, current_app
from src.expense.schemas import ExpenseSchema, ExpenseListSchema
from src.expense.models import Expense
from src.utils.helpers import get_response_obj
from sqlalchemy.exc import SQLAlchemyError
from src.common.models import db
from src.auth.api import AuthResource


class ExpenseResource(Resource):

    def get(self, expense_id):
        expense = Expense.query.filter_by(id=expense_id).first()
        expense_schema = ExpenseSchema()
        if not expense:
            return get_response_obj("No expenses found for the user", error="No expense"), 404

        return (
            get_response_obj("expense data", data=expense_schema.dump(expense)),
            200,
        )


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
        expenses = Expense.query.filter_by(user_id=current_user.id).all()
        return (
            get_response_obj("expense list", data=expense_schema.dump(expenses, many=True)),
            200,
        )
