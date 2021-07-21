"""
Author: Nachiket Panchal
"""
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from marshmallow import ValidationError
from flask import g
from flask_restful import Resource, request, current_app
from src.income.schemas import IncomeSchema, IncomeListSchema
from src.income.models import Income
from src.utils.helpers import get_response_obj
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from src.common.models import db
from src.auth.api import AuthResource


class IncomeResource(Resource):

    def get(self, income_id):
        income = Income.query.filter_by(id=income_id).first()
        income_schema = IncomeSchema()
        if not income:
            return get_response_obj("No income found", error="No income with given id"), 404

        return (
            get_response_obj("income data", data=income_schema.dump(income)),
            200,
        )

    def delete(self, income_id):
        income = Income.query.get(income_id)
        if not income:
            return get_response_obj("No income found", error="No income with given id"), 404

        try:
            income.delete()
        except SQLAlchemyError as e:
            current_app.logger.exception("Error deleting income")
            return get_response_obj(
                "Server error while deleting income",
                error="Database error",
            ), 500

        return get_response_obj("Income deleted", data=None), 200

class IncomeListResource(AuthResource):

    def post(self):
        income_schema = IncomeSchema()
        current_user = g.current_user
        try:
            income = income_schema.load(request.json or {}, session=db.session())
        except ValidationError as e:
            return get_response_obj(
                "Cannot create an income entry. Invalid request data",
                error=e.messages,
            ), 422
        income.user_id = current_user.id # assign income to current user
        try:
            income.add()
        except SQLAlchemyError as e:
            current_app.logger.exception("Error creating income")
            return (
                get_response_obj(
                    "Error creating an expense entry, Server error",
                    error="Server error",
                ),
                500,
            )

        return (
            get_response_obj("Income created", data=income_schema.dump(income)),
            200,
        )

    def get(self):
        current_user = g.current_user
        income_schema = IncomeSchema()
        try:
            req_args = IncomeListSchema().load(request.args or {})
        except ValidationError as e:
            current_app.logger.exception("Invalid request params")
            return get_response_obj("Invalid request params", error=e.messages), 422

        # create two dates representing first and last date of requested month
        start_date = date(req_args["date"].year, req_args["date"].month, 1)
        next_month_date = start_date + relativedelta(months=1)
        end_date = date(next_month_date.year, next_month_date.month, 1)
        current_app.logger.info("Listing income from %s to %s", start_date, end_date)

        income = (
            Income.query.filter_by(user_id=current_user.id)
            .filter(
                and_(
                    Income.date >= start_date,
                    Income.date < end_date
                )
            )
            .all()
        )
        return (
            get_response_obj("income list", data=income_schema.dump(income, many=True)),
            200,
        )
