from marshmallow import ValidationError
from flask_restful import Resource, request, current_app
from src.expense.schemas import ExpenseSchema
from src.expense.models import Expense
from src.utils.helpers import get_response_obj
from sqlalchemy.exc import SQLAlchemyError
from app import db


class ExpenseResource(Resource):

    def get(self, user_id):
        expense = Expense.query.filter_by(user_id=user_id).all()
        expense_schema = ExpenseSchema(many=True)
        print(expense)
        print(type(expense))
        print(expense_schema.dump(expense))
        if not expense:
            return get_response_obj("No expenses found for the user", error="No user"), 404

        return (
            get_response_obj("expense data", data=expense_schema.dump(expense)),
            200,
        )
class AddExpenseResource(Resource):

    def post(self):
        expense_schema = ExpenseSchema()
        try:
            expense = expense_schema.load(request.json or {}, session=db.session())
        except ValidationError as e:
            return get_response_obj(
                "Cannot create an expense entry. Invalid request data",
                error=e.messages,
            ), 422
        try:
            session = db.session()
            session.add(expense)
            session.commit()
        except SQLAlchemyError as e:
            current_app.logger.exception("Error creating expense")
            return (
                get_response_obj(
                    "Error creating an expense entry, Server error",
                    error="Server errro",
                ),
                500,
            )

        return (
            get_response_obj("Expense created", data=expense_schema.dump(expense)),
            200,
        )
