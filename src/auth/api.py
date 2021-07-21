"""
Author: Rushikesh Patel
"""
from flask_restful import Resource
from src.auth.decorators import load_current_user


class AuthResource(Resource):
    # base resource class to create protected api endpoints

    method_decorators = [load_current_user]
