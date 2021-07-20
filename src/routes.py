from flask import Blueprint
from flask_restful import Api
from src.users.views import UserResource, CreateUserResource, LoginResource

# user api endpoints
user_bp = Blueprint("user_bp", __name__)
api = Api(user_bp)

api.add_resource(UserResource, "/<user_id>")
api.add_resource(CreateUserResource, "")
api.add_resource(LoginResource, "/login")