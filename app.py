from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
CORS(app)
api = Api(app)

def hello_world():
    return {"message": "hello world"}

app.add_url_rule("/", "helloworld", hello_world, methods=["GET", "POST"])

if __name__ == "__main__":
    app.run()