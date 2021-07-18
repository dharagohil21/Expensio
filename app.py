from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config.from_object("src.configs.config")

# database configuration
db = SQLAlchemy(app)

def hello_world():
    return {"message": "hello world"}

app.add_url_rule("/", "helloworld", hello_world, methods=["GET", "POST"])

# register blueprint routes
from src import routes
app.register_blueprint(routes.user_bp, url_prefix="/users")
app.register_blueprint(routes.expense_bp, url_prefix="/expense")

if __name__ == "__main__":
    app.run()
