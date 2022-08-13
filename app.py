import os
from flask import Flask, jsonify
from flask_migrate import Migrate

from models import setup_db, db, Actors


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    @app.route('/')
    def index():
        return 'hello there!'

    @app.route('/actors')
    def get_actors():
        actors = Actors.query.all()
        return jsonify({
            'actors': [actor.format() for actor in actors]
        })

    return app


app = create_app()
migrate = Migrate()
migrate.init_app(app, db)

if __name__ == '__main__':
    app.run(debug=True if os.getenv('DEBUG') == 'true' else False)
