import os
from http import HTTPStatus

from flask import Flask, request, jsonify, abort, render_template, redirect
from flask_migrate import Migrate

from auth import AUTH0_LOGIN_URL
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
    def get_actors():
        actors = Actor.query.all()
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        })

    @app.route('/actors', methods=['POST'])
    def create_actor():
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
                'movie': actor.format()
            }), HTTPStatus.CREATED
        except Exception as ex:
            print(ex)
            abort(HTTPStatus.UNPROCESSABLE_ENTITY)

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    def get_actor(actor_id):
        actor = Actor.query.get_or_404(actor_id)
        return jsonify(actor.format())

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def update_actor(actor_id):
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
    def delete_actor(actor_id):
        actor = Actor.query.get_or_404(actor_id)
        actor.delete()
        return jsonify(), HTTPStatus.NO_CONTENT

    @app.route('/movies')
    def get_movies():
        movies = Movie.query.all()
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        })

    @app.route('/movies', methods=['POST'])
    def create_movie():
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
    def get_movie(movie_id):
        movie = Movie.query.get_or_404(movie_id)
        return jsonify(movie.format())

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def update_movie(movie_id):
        form = MovieForm(request.form)
        if not form.validate():
            return jsonify(form.errors), HTTPStatus.BAD_REQUEST

        movie = Actor.query.get_or_404(movie_id)
        movie.title = form.title.data
        movie.release_date = form.release_date.data

        movie.update()
        return jsonify(movie.format())

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        movie = Movie.query.get_or_404(movie_id)
        movie.delete()
        return jsonify(), HTTPStatus.NO_CONTENT

    return app


app = create_app()
migrate = Migrate()
migrate.init_app(app, db)

if __name__ == '__main__':
    app.run(debug=True if os.getenv('DEBUG') == 'true' else False)
