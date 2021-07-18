from main import init_app

app = init_app("src.configs.config")

def hello_world():
    return {"message": "hello world"}

app.add_url_rule("/", "helloworld", hello_world, methods=["GET", "POST"])

# register blueprint routes
from src import routes
app.register_blueprint(routes.user_bp, url_prefix="/user")

if __name__ == "__main__":
    app.run()
