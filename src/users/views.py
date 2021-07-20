from hashlib import sha1
from marshmallow import ValidationError
from flask_restful import Resource, request, current_app
from src.users.schemas import UserSchema
from src.users.models import User
from src.utils.helpers import get_response_obj
from sqlalchemy.exc import SQLAlchemyError
from src.common.models import db
from src.users.schemas import LoginSchema
from flask_jwt_extended import create_access_token
from src.auth.api import AuthResource


class UserResource(AuthResource):

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

        # hash password
        user.password = sha1(user.password.encode()).hexdigest()
        try:
            user.add()
        except SQLAlchemyError as e:
            current_app.logger.exception("Error creating user")
            return (
                get_response_obj(
                    "Error creating user, Server error",
                    error="Server error",
                ),
                500,
            )

        return (
            get_response_obj("User created", data=user_schema.dump(user)),
            200,
        )

    def put(self, user_id):
        user_schema = UserSchema()
        try:
            update_user = user_schema.load(request.json or {}, session=db.session(), partial=True)
        except ValidationError as e:
            return get_response_obj(
                "Cannot create user. Invalid request data",
                error=e.messages,
            ), 422

        user = User.query.get(user_id)
        if update_user.name != user.name:
            user.name = update_user.name
        if update_user.email != user.email:
            user.email = update_user.email
        if sha1(update_user.password).hexdigest() != user.password:
            user.password = sha1(update_user.password).hexdigest()

        try:
            user.update()
        except SQLAlchemyError as e:
            current_app.logger.exception("Error updating user")
            return (
                get_response_obj(
                    "Error creating user, Server error",
                    error="Server error",
                ),
                500,
            )

        return (
            get_response_obj("User updated", data=user_schema.dump(user)),
            200,
        )


class LoginResource(Resource):

    def post(self):
        login_schema = LoginSchema()
        try:
            login_details = login_schema.load(request.json or {})
        except ValidationError as e:
            current_app.logger.exception("Invalid login data")
            return get_response_obj(
                "Login failed. Invalid request data",
                error="missing required fields",
            ), 401
        hashed_password = sha1(login_details["password"].encode()).hexdigest()
        user = User.query.filter_by(
            email=login_details["email"],
            password=hashed_password,
        ).first()
        if not user:
            return get_response_obj(
                "Cannot login, unknown user",
                error="user not found with given credentials",
            ), 401
        token = create_access_token(identity={"id":user.id})
        return get_response_obj(
            "Login successful",
            data = {"token": token},
        ), 200
