import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS

from models import setup_db, Movies, Actors
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    '''
  Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
  GET /actors
  '''
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        # get all actors
        all_actors = Actors.query.all()

        # resource not found error (if there is no actors)
        if all_actors is None:
            abort(400)

        actors_list = {}
        for actors in all_actors:
            #actors_list = actors.name
            #actors_list[actors.id] = actors.name
            actors_list[actors.id] = [
                actors.name, actors.age, actors.gender]

        if len(actors_list) == 0:
            abort(404)

        # No error, return success true and actors_list
        return jsonify({
            'success': True,
            'actors': actors_list
        })

    '''
  GET /movies
  '''
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        # get all actors
        all_movies = Movies.query.all()

        # resource not found error (if there is no movies)
        if all_movies is None:
            abort(400)

        movies_list = {}

        for movies in all_movies:
            movies_list[movies.id] = [
                movies.title, movies.date]

        if len(movies_list) == 0:
            abort(404)

        # No error, return success true and movies_list
        return jsonify({
            'success': True,
            'movies': movies_list
        })

    '''
  DELETE /actors
  '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        try:
            # get the actor
            actor = Actors.query.filter_by(
                id=actor_id).one_or_none()

            # resource not found error (no actor found with
            # this id)
            if actor is None:
                abort(404)

            actor.delete()

            # No error, return success true and deleted
            # actor_id
            return jsonify({
                'success': True,
                'deleted': actor_id
            })

        except BaseException:
            # unprocessable error
            abort(422)

    '''
  DELETE /movies
  '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        try:
            # get the actor
            movie = Movies.query.filter_by(
                id=movie_id).one_or_none()

            # resource not found error (no movie found with
            # this id)
            if movie is None:
                abort(404)

            movie.delete()

            # No error, return success true and deleted
            # actor_id
            return jsonify({
                'success': True,
                'deleted': movie_id
            })

        except BaseException:
            # unprocessable error
            abort(422)

    '''
  POST /actors
  '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        body = request.get_json()

        # get all the user's inputs
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        # check the user's inputs
        if new_name == '' or new_age == '' or new_gender == '':
            # unprocessable error
            abort(422)

        try:
            actor = Actors(
                name=new_name,
                age=new_age,
                gender=new_gender)
            actor.insert()

            total = len(Actors.query.all())

            return jsonify({
                'success': True,
                'created': actor.id,
                'totalActors': total
            })

        except BaseException:
            # unprocessable error
            abort(422)

    '''
  POST /movies
  '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        body = request.get_json()

        # get all the user's inputs
        new_title = body.get('title', None)
        new_date = body.get('date', None)

        # check the user's inputs
        if new_title == '' or new_date == '':
            # unprocessable error
            abort(422)

        try:
            movie = Movies(title=new_title, date=new_date)
            movie.insert()

            total = len(Movies.query.all())

            return jsonify({
                'success': True,
                'created': movie.id,
                'totalMovies': total
            })

        except BaseException:
            # unprocessable error
            abort(422)

    '''
  PATCH /actors
  '''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(payload, actor_id):
        body = request.get_json()

        # get all the user's inputs
        new_age = body.get('age', None)

        actor = Actors.query.filter_by(
            id=actor_id).one_or_none()

        # resource not found error (no drink found with this
        # id)
        if actor is None:
            abort(404)

        actor.age = new_age
        actor.update()

        return jsonify({
            'success': True,
            'id': actor.id,
            'age': actor.age
        })

    '''
  PATCH /movies
  '''
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(payload, movie_id):
        body = request.get_json()

        # get all the user's inputs
        new_title = body.get('title', None)

        movie = Movies.query.filter_by(
            id=movie_id).one_or_none()

        # resource not found error (no drink found with this
        # id)
        if movie is None:
            abort(404)

        movie.title = new_title
        movie.update()

        return jsonify({
            'success': True,
            'id': movie.id,
            'title': movie.title
        })

    '''
  Handling Errors
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not found"
        }), 405

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['code']
        }), 403

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=8080, debug=True)
