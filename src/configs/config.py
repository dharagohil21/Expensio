"""
Author: Rushikesh Patel
"""
from os import environ as env
from datetime import timedelta

SECRET_KEY = "+zCiaBZ0JNVUzi6VdqMJrJs7Nv3oDHDXCwwaOTlzhx3kKFz3I33m9"
JWT_SECRET_KEY = "JrJs7Nv3oDHDXCwwaOTlzhx3kKFz"

DB_HOST = env["DB_HOST"]
DB_USER = env["DB_USER"]
DB_PASS = env["DB_PASS"]
DB_NAME = env["DB_NAME"]

SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365)
JWT_TOKEN_LOCATION = "headers"