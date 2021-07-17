from marshmallow import ValidationError
from flask_restful import Resource, request, current_app
from src.users.schemas import UserSchema
from src.users.models import User
from src.utils.helpers import get_response_obj
from sqlalchemy.exc import SQLAlchemyError
from app import db


class UserResource(Resource):

    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        user_schema = UserSchema()

        if not user:
            return get_response_obj("No user found", error="No user"), 404

        return (
            get_response_obj("User data", data=user_schema.dump(user)),
            200,
        )


class CreateUserResource(Resource):

    def post(self):
        user_schema = UserSchema()
        try:
            user = user_schema.load(request.json or {}, session=db.session())
        except ValidationError as e:
            return get_response_obj(
                "Cannot create user. Invalid request data",
                error=e.messages,
            ), 422
        try:
            session = db.session()
            session.add(user)
            session.commit()
        except SQLAlchemyError as e:
            current_app.logger.exception("Error creating user")
            return (
                get_response_obj(
                    "Error creating user, Server error",
                    error="Server errro",
                ),
                500,
            )

        return (
            get_response_obj("User created", data=user_schema.dump(user)),
            200,
        )
