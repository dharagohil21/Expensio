"""
Author: Nachiket Panchal, Jaspreet Kaur Gill, Rushikesh Patel
"""
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from marshmallow import ValidationError
from flask import g
from flask_restful import request, current_app
from src.income.schemas import IncomeSchema, IncomeListSchema, IncomeCategorySchema
from src.income.models import Income, IncomeCategory
from src.utils.helpers import get_response_obj
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from src.common.models import db
from src.auth.api import AuthResource


class IncomeResource(AuthResource):

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
        current_user = g.current_user
        if not income:
            return get_response_obj("No income found", error="No income with given id"), 404

        try:
            next_month_date = income.date + relativedelta(months=1)
            next_month_start = date(next_month_date.year, next_month_date.month, 1)
            # delete the future entires if the the income is recurring
            Income.query.filter(
                and_(
                    Income.user_id == current_user.id,
                    Income.date >= next_month_start,
                    Income.amount == income.amount,
                    Income.income_category == income.income_category,
                    Income.title == income.title,
                )
            ).delete()
            income.delete()
        except SQLAlchemyError as e:
            current_app.logger.exception("Error deleting income")
            return get_response_obj(
                "Server error while deleting income",
                error="Database error",
            ), 500

        return get_response_obj("Income deleted", data=None), 200

    def put(self, income_id):
        income = Income.query.filter_by(id=income_id).first()
        if not income:
            return get_response_obj("No incomes found", error="No income with given id"), 404

        income_schema = IncomeSchema()
        try:
            req_data = request.json
            new_income = income_schema.load(req_data, session=db.session, partial=True)
        except ValidationError as e:
            current_app.logger.exception("Cannot update income, invalid request data")
            return get_response_obj(
                "Cannot update income, invalid request data",
                error=e.messages,
            ), 422

        if "title" in req_data and new_income.title != income.title:
            income.title = new_income.title
        if "amount" in req_data and new_income.amount != income.amount:
            income.amount = new_income.amount

        try:
            current_user = g.current_user
            if "is_recurring" in req_data and new_income.is_recurring != income.is_recurring:
                # if is_recurring flag is being modified
                income.is_recurring = new_income.is_recurring
                if new_income.is_recurring is False:
                    # when recurring flag is changed from true to false
                    next_month_date = income.date + relativedelta(months=1)
                    next_month_start = date(next_month_date.year, next_month_date.month, 1)
                    # delete the recurring entries of the income entry from the future months
                    Income.query.filter(
                        and_(
                            Income.user_id == current_user.id,
                            Income.date >= next_month_start,
                            Income.amount == income.amount,
                            Income.income_category == income.income_category,
                            Income.title == income.title
                        )
                    ).delete()
            income.update()
        except SQLAlchemyError as e:
            current_app.logger.exception("Error updating income")
            return get_response_obj(
                "Server error while updating income",
                error="Database error"
            ), 500

        return get_response_obj("Income updated", data=income_schema.dump(income)), 200


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
                    "Error creating an income entry, Server error",
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

        current_month_income = (
            Income.query.filter_by(user_id=current_user.id)
            .filter(
                and_(
                    Income.date >= start_date,
                    Income.date < end_date
                )
            )
            .all()
        )
        if start_date >= date.today(): # if future date
            prev_month_recurr_incomes = Income.query.filter(
                and_(
                    Income.date >= start_date + relativedelta(months=-1),
                    Income.date < start_date,
                    Income.is_recurring == True,
                    Income.user_id == current_user.id
                )
            ).all()
            new_incomes = list()
            for inc in prev_month_recurr_incomes:
                # iterate through prev month recurring incomes,
                # and replay those entries to requested month
                # if not present
                matched_income = next(
                    (
                        e for e in current_month_income
                        if e.amount == inc.amount
                        and e.income_category == inc.income_category
                        and e.title == inc.title
                    ),
                    None,
                )
                if matched_income is not None:
                    current_app.logger.info("Recurring income entry found")
                    continue

                income = Income(
                    user_id=current_user.id,
                    title=inc.title,
                    amount=inc.amount,
                    income_category=inc.income_category,
                    is_recurring=True,
                    date=start_date,
                )
                new_incomes.append(income)
                current_app.logger.info("creating new recurring income")
            try:
                session = db.session
                session.add_all(new_incomes)
                session.commit()
                current_month_income += new_incomes
            except SQLAlchemyError as e:
                current_app.logger.exception("Error creating recurring income")
                return get_response_obj("Server error listing income", error="Database error"), 500


        return (
            get_response_obj("income list", data=income_schema.dump(current_month_income, many=True)),
            200,
        )


class IncomeCategoryListResource(AuthResource):

    def get(self):
        income_categories = IncomeCategory.query.all()
        schema = IncomeCategorySchema()
        return get_response_obj("Income categories", data=schema.dump(income_categories, many=True))

    def post(self):
        schema = IncomeCategorySchema()
        try:
            category = schema.load(request.json or {}, session=db.session)
        except ValidationError as e:
            return get_response_obj(
                "Cannot create an income category. Invalid request data",
                error=e.messages,
            ), 422
        try:
            category.add()
        except SQLAlchemyError as e:
            current_app.logger.exception("Error creating income category")
            return (
                get_response_obj(
                    "Error creating an income category, Server error",
                    error="Server error",
                ),
                500,
            )

        return (
            get_response_obj("Income category created", data=schema.dump(category)),
            200,
        )


class IncomeCategoryResource(AuthResource):

        def delete(self, category_id):
            category = IncomeCategory.query.get(category_id)
            if not category:
                return get_response_obj("No income category found", error="No category with given id"), 404

            try:
                category.delete()
            except SQLAlchemyError as e:
                current_app.logger.exception("Error deleting income category")
                return get_response_obj(
                    "Server error while deleting income category",
                    error="Database error",
                ), 500

            return get_response_obj("Income category deleted", data=None ), 200
