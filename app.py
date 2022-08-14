import os
from http import HTTPStatus

from flask import Flask, request, jsonify, abort, render_template, redirect
from flask_migrate import Migrate

from auth import AUTH0_LOGIN_URL, requires_auth, AuthError
from forms import ActorForm, MovieForm
from models import setup_db, db, Actor, Movie


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login')
    def login():
        return redirect(AUTH0_LOGIN_URL)

    @app.route('/actors')
    @requires_auth('read:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actor')
    def create_actor(payload):
        form = ActorForm(request.form)
        if not form.validate():
            return jsonify(form.errors), HTTPStatus.BAD_REQUEST
        try:
            actor = Actor(name=form.name.data, age=form.age.data,
                          gender=form.gender.data)
            actor.insert()
            return jsonify({
                'success': True,
                'message': f'Actor {actor.name} created.',
                'actor': actor.format()
            }), HTTPStatus.CREATED
        except Exception as ex:
            print(ex)
            abort(HTTPStatus.UNPROCESSABLE_ENTITY)

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('read:actors')
    def get_actor(payload, *args, **kwargs):
        actor_id = kwargs.get('actor_id')
        actor = Actor.query.get_or_404(actor_id)
        return jsonify(actor.format())

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actor')
    def update_actor(payload, *args, **kwargs):
        actor_id = kwargs.get('actor_id')
        form = ActorForm(request.form)
        if not form.validate():
            return jsonify(form.errors), HTTPStatus.BAD_REQUEST

        actor = Actor.query.get_or_404(actor_id)
        actor.name = form.name.data
        actor.age = form.age.data
        actor.gender = form.gender.data

        actor.update()
        return jsonify(actor.format())

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, *args, **kwargs):
        actor_id = kwargs.get('actor_id')
        actor = Actor.query.get_or_404(actor_id)
        actor.delete()
        return jsonify(), HTTPStatus.NO_CONTENT

    @app.route('/movies')
    @requires_auth('read:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movie')
    def create_movie(payload):
        form = MovieForm(request.form)
        if not form.validate():
            return jsonify(form.errors), HTTPStatus.BAD_REQUEST
        try:
            movie = Movie(title=form.title.data,
                          release_date=form.release_date.data)
            movie.insert()
            return jsonify({
                'success': True,
                'message': f'Movie {movie.title} created.',
                'movie': movie.format()
            }), HTTPStatus.CREATED
        except Exception as ex:
            print(ex)
            abort(HTTPStatus.UNPROCESSABLE_ENTITY)

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('read:movies')
    def get_movie(payload, *args, **kwargs):
        movie_id = kwargs.get('movie_id')
        movie = Movie.query.get_or_404(movie_id)
        return jsonify(movie.format())

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movie')
    def update_movie(payload, *args, **kwargs):
        movie_id = kwargs.get('movie_id')
        form = MovieForm(request.form)
        if not form.validate():
            return jsonify(form.errors), HTTPStatus.BAD_REQUEST

        movie = Movie.query.get_or_404(movie_id)
        movie.title = form.title.data
        movie.release_date = form.release_date.data

        movie.update()
        return jsonify(movie.format())

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, *args, **kwargs):
        movie_id = kwargs.get('movie_id')
        movie = Movie.query.get_or_404(movie_id)
        movie.delete()
        return jsonify(), HTTPStatus.NO_CONTENT

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            'success': False,
            'error': error.err_code,
            'message': error.description
        }), error.status_code

    return app


app = create_app()
migrate = Migrate()
migrate.init_app(app, db)

if __name__ == '__main__':
    app.run(debug=True if os.getenv('DEBUG') == 'true' else False)
