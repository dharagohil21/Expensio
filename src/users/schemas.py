from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields
from src.users.models import User

class UserSchema(SQLAlchemyAutoSchema):
    id = fields.Integer(dump_only=True) # read-only by user request
    password = fields.String(load_only=True, required=True)

    class Meta:
        model = User
        include_relationships = False
        include_fk = True
        load_instance = True

class LoginSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)