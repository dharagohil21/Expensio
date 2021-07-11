from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__, static_folder="frontend/build")
CORS(app)
api = Api(app)

from backend.hello import HelloWorld

api.add_resource(HelloWorld, "/hello")

@app.route("/", defaults={"path": ''})
def root(path):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run()