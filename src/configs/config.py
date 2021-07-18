from os import environ as env

SECRET_KEY = "+zCiaBZ0JNVUzi6VdqMJrJs7Nv3oDHDXCwwaOTlzhx3kKFz3I33m9"

#DB_HOST = env["DB_HOST"]
#DB_USER = env["DB_USER"]
#DB_PASS = env["DB_PASS"]
#DB_NAME = env["DB_NAME"]##

#SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://root:Chinky30891$@localhost/5709_project"

SQLALCHEMY_TRACK_MODIFICATIONS = False
