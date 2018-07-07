from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    @app.route("/")
    def hello():
        return "Hello!"
    return app

if __name__ == "__main__":
    create_app().run()
