"""Expose and consume movie data in JSON format."""

__author__ = "Filipe Bezerra de Sousa"

from flask import jsonify, request, current_app
from flask.helpers import url_for
from sqlalchemy.exc import StatementError
from app import db, cache
from app.api import bp
from app.models import Movie
from app.api.errors import not_found
from app.auth.auth import auth_required
from app.integrations.flask_caching import (
    redis_is_not_available, redis_is_available)


@bp.route('/movies')
@auth_required('view:movies')
@cache.memoize(unless=redis_is_not_available)
def get_movies():
    """Get a list of Movie.
    ---
    tags:
      - movies
    definitions:
      Movie:
        type: object
        properties:
          actors:
            type: list
            example: [{"age":56,"fullName":"Keanu Reeves",
            "gender":"Male","moviesCount":1,"uuid":"aedc900e-7fe7-4af5-a556-3d606118f3dc"}
            ,{"age":54,"fullName":"Halle Berry","gender":"Female","moviesCount":1,
            "uuid":"75005dc2-2b37-423c-815f-04b677737eac"},{"age":77,"fullName":
            "Ian McShane","gender":"Male","moviesCount":1,"uuid":"cb0c1dca-d058-4505-99b6-024c94a522ac"}
            ,{"age":59,"fullName":"Laurence Fishburne","gender":"Male","moviesCount":1
            ,"uuid":"0609f0f6-dc13-4c35-8bc7-9396ff55739d"},{"age":56,"fullName":
            "Mark Dacascos","gender":"Male","moviesCount":1,"uuid":"cc16790f-2699-4db2-afc7-05c8e34439e6"}
            ,{"age":35,"fullName":"Asia Kate Dillon","gender":"Female","moviesCount":1
            ,"uuid":"208c4f74-7106-4a0e-96ae-b333815f2efc"},{"age":57,"fullName":"Lance Reddick",
            "gender":"Male","moviesCount":1,"uuid":"42ebc19d-0ca1-44ff-b665-ee329d3d9806"}]
          releaseDate:
            type: date
            pattern: /([0-9]{4})-(?:[0-9]{2})-([0-9]{2})/
            example: "2019-05-17"
          title:
            type: string
            example: "John Wick: Chapter 3 - Parabellum"
          uuid:
            type: string
            example: "941f7036-a3a2-44f0-8eb7-e2b41f3ab59c"
    produces:
      - application/json
    responses:
      200:
        description: A dictionary with a ``objects`` attribute which is the 
            ``list`` of movies and a ``page``, ``totalCount``, ``totalPages`` 
            meta attributes.
        schema:
          type: object
          properties:
            objects:
              type: array
              items:
                $ref: '#/definitions/Movie'
              example: [{"actors":[{"age":56,"fullName":"Keanu Reeves",
              "gender":"Male","moviesCount":1,"uuid":"aedc900e-7fe7-4af5-a556-3d606118f3dc"}
              ,{"age":54,"fullName":"Halle Berry","gender":"Female","moviesCount":1,
              "uuid":"75005dc2-2b37-423c-815f-04b677737eac"},{"age":77,"fullName":
              "Ian McShane","gender":"Male","moviesCount":1,"uuid":"cb0c1dca-d058-4505-99b6-024c94a522ac"}
              ,{"age":59,"fullName":"Laurence Fishburne","gender":"Male","moviesCount":1
              ,"uuid":"0609f0f6-dc13-4c35-8bc7-9396ff55739d"},{"age":56,"fullName":
              "Mark Dacascos","gender":"Male","moviesCount":1,"uuid":"cc16790f-2699-4db2-afc7-05c8e34439e6"}
              ,{"age":35,"fullName":"Asia Kate Dillon","gender":"Female","moviesCount":1
              ,"uuid":"208c4f74-7106-4a0e-96ae-b333815f2efc"},{"age":57,"fullName":"Lance Reddick",
              "gender":"Male","moviesCount":1,"uuid":"42ebc19d-0ca1-44ff-b665-ee329d3d9806"}],
              "releaseDate":"2019-05-17","title":"John Wick: Chapter 3 - Parabellum",
              "uuid":"941f7036-a3a2-44f0-8eb7-e2b41f3ab59c"}]
            page:
              type: integer
              example: 1
            totalCount:
              type: integer
              example: 2
            totalPages:
              type: integer
              example: 1
      401:
        description: If the user is not authenticated.
      403:
        description: If the authenticated user is now allowed to access this 
            resource.
      500:
        description: Something goes wrong within our end.

    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get(
        'limit', current_app.config['THECREW_OBJECTS_PER_PAGE'], type=int)
    pagination = Movie.query.paginate(page, per_page=limit, error_out=False)

    result_dict = {
        'objects': [movie.to_json() for movie in pagination.items],
        'totalCount': pagination.total,
        'totalPages': pagination.pages,
        'page': pagination.page
    }
    if pagination.has_prev:
        result_dict['prevLink'] = url_for(
            'api.get_movies', page=pagination.prev_num)
    if pagination.has_next:
        result_dict['nextLink'] = url_for(
            'api.get_movies', page=pagination.next_num)

    return jsonify(result_dict)


@bp.route('movies/<string:movie_id>')
@auth_required('view:movies')
@cache.memoize(unless=redis_is_not_available)
def get_movie(movie_id):
    """Get a existing Movie.
    The appropriate ``ID`` format must be given, for example: ``941f7036-a3a2-44f0-8eb7-e2b41f3ab59c``
    ---
    tags:
      - movies
    parameters:
      - name: movie_id
        in: path
        description: The `ID` of a existing movie.
        example: 941f7036-a3a2-44f0-8eb7-e2b41f3ab59c
    produces:
      - application/json
    responses:
      200:
        description: A dictionary with the movie attributes.
        schema:
          type: object
          $ref: '#/definitions/Movie'
      401:
        description: if the user is not authenticated.
      403:
        description: If the authenticated user is now allowed to access this 
            resource.
      404:
        description: If the movie ``ID`` does not exist or using an invalid 
            format.
      500:
        description: Something goes wrong within our end.

    """
    movie = None
    try:
        movie = Movie.query.filter_by(uuid=movie_id).first_or_404()
    except StatementError:
        return not_found('please use the correct path parameter')
    return jsonify(movie.to_json())


@bp.route('/movies', methods=['POST'])
@auth_required('add:movies')
def create_movie():
    """Create a new Movie using the submitted attributes.
    All attributes are mandatory.
    ---
    tags:
      - movies
    parameters:
      - name: body
        in: body
        description: The Movie JSON attributes.
        schema:
          properties:
            actors:
              type: list
              description: A list of objects containing at least the ID of each Actor.
              required: true
              example: [{"uuid":"aedc900e-7fe7-4af5-a556-3d606118f3dc"},
              {"uuid":"75005dc2-2b37-423c-815f-04b677737eac"},
              {"uuid":"cb0c1dca-d058-4505-99b6-024c94a522ac"}]
            releaseDate:
              type: date
              pattern: /([0-9]{4})-(?:[0-9]{2})-([0-9]{2})/
              description: The date when the Movie was release.
              required: true
              example: "2019-05-17"
            title:
              type: string
              description: The title of the Movie.
              required: true
              example: "John Wick: Chapter 3 - Parabellum"
    consumes:
      - application/json  
    produces:
      - application/json
    responses:
      200:
        description: A dictionary with the movie attributes.
        schema:
          type: object
          $ref: '#/definitions/Movie'
      400:
        description: If one of the required parameters were missing, or the movie 
          already.
      401:
        description: If the user is not authenticated.
      403:
        description: if the authenticated user is now allowed to access this 
            resource.
      500:
        description: Something goes wrong within our end.

    """
    json_movie = request.json or {}
    movie = Movie.new_from_json(json_movie)
    db.session.commit()
    if redis_is_available():
        cache.delete_memoized(get_movies)
    return jsonify(movie.to_json()), 201, \
        {'Location': url_for('api.get_movie', movie_id=str(movie.uuid))}


@bp.route('/movies/<string:movie_id>', methods=['PATCH'])
@auth_required('edit:movies')
def update_movie(movie_id):
    """Update an existing Movie using the the submitted attributes.
    Can update either only the actors, the release date or the title.
    
    The appropriate ``ID`` format must be given, for example: ``941f7036-a3a2-44f0-8eb7-e2b41f3ab59c``
    ---
    tags:
      - movies
    parameters:
      - name: movie_id
        in: path
        description: The `ID` of a existing movie.
        example: 941f7036-a3a2-44f0-8eb7-e2b41f3ab59c
      - name: body
        in: body
        description: The Movie JSON attributes. Could contain only the actors,
            the releaseDate, the title, or even all of them.
        schema:
          properties:
            actors:
              type: list
              description: A list of objects containing at least the ID of each Actor.
              example: [{"uuid":"aedc900e-7fe7-4af5-a556-3d606118f3dc"},
              {"uuid":"75005dc2-2b37-423c-815f-04b677737eac"},
              {"uuid":"cb0c1dca-d058-4505-99b6-024c94a522ac"}]
            releaseDate:
              type: date
              pattern: /([0-9]{4})-(?:[0-9]{2})-([0-9]{2})/
              description: The date when the Movie was release.
              example: "2019-05-17"
            title:
              type: string
              description: The title of the Movie.
              example: "John Wick: Chapter 3 - Parabellum"
    consumes:
      - application/json  
    produces:
      - application/json
    responses:
      200:
        description: A dictionary with the movie attributes.
        schema:
          type: object
          $ref: '#/definitions/Movie'
      400:
        description: If one of the required parameters were missing, or the movie already.
      401:
        description: If the user is not authenticated.
      403:
        description: if the authenticated user is now allowed to access this 
            resource.
      404:
        description: If the movie ``ID`` does not exist or using an invalid 
            format.
      500:
        description: Something goes wrong within our end.

    """
    movie = None
    try:
        movie = Movie.query.filter_by(uuid=movie_id).first_or_404()
    except StatementError:
        return not_found('please use the correct path parameter')
    json_movie = request.json or {}
    movie.update_from_json(json_movie)
    db.session.commit()
    if redis_is_available():
        cache.delete_memoized(get_movies)
        cache.delete_memoized(get_movie, movie_id)
    return jsonify(movie.to_json())


@bp.route('/movies/<string:movie_id>', methods=['DELETE'])
@auth_required('delete:movies')
def delete_movie(movie_id):
    """Deletes an existing Movie.
    The appropriate ``ID`` format must be given, for example: ``941f7036-a3a2-44f0-8eb7-e2b41f3ab59c``
    ---
    tags:
      - movies
    parameters:
      - name: movie_id
        in: path
        description: The `ID` of a existing movie.
        example: 941f7036-a3a2-44f0-8eb7-e2b41f3ab59c
    responses:
      200:
        description: No content.
      401:
        description: if the user is not authenticated.
      403:
        description: If the authenticated user is now allowed to access this 
            resource.
      404:
        description: If the movie ``ID`` does not exist or using an invalid 
            format.
      500:
        description: Something goes wrong within our end.

    """
    movie = None
    try:
        movie = Movie.query.filter_by(uuid=movie_id).first_or_404()
    except StatementError:
        return not_found('please use the correct path parameter')
    db.session.delete(movie)
    db.session.commit()
    if redis_is_available():
        cache.delete_memoized(get_movies)
        cache.delete_memoized(get_movie, movie_id)
    return '', 204
