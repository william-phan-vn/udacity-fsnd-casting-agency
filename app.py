from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config')

    @app.route('/')
    def index():
        return 'hello there'


    return app


app = create_app()


if __name__ == '__main__':
    app.run()
