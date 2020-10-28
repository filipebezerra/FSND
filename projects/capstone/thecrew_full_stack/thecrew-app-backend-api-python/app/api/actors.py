"""Expose and consume actor data in JSON format."""

__author__ = "Filipe Bezerra de Sousa"

from flask import jsonify, request, current_app
from flask.helpers import url_for
from sqlalchemy.exc import StatementError
from app import db, cache
from app.api import bp
from app.models import Actor
from app.api.errors import not_found
from app.auth.auth import auth_required
from app.integrations.flask_caching import (
    redis_is_not_available, redis_is_available)


@bp.route('/actors')
@auth_required('view:actors')
@cache.memoize(unless=redis_is_not_available)
def get_actors():
    """Get a list of Actor.
    ---
    tags:
      - actors
    definitions:
      Actor:
        type: object
        properties:
          age:
            type: integer
            example: 56
          fullName:
            type: string
            example: "Keanu Reeves"
          gender:
            type: string
            example: "Male"
          moviesCount:
            type: integer
            example: 1
          uuid:
            type: string
            example: "2f607b49-771d-4b96-9692-715ea2b38210"
    produces:
      - application/json
    responses:
      200:
        description: A dictionary with a ``objects`` attribute which is the 
            ``list`` of actors and a ``page``, ``totalCount``, ``totalPages`` 
            meta attributes.
        schema:
          type: object
          properties:
            objects:
              type: array
              items:
                $ref: '#/definitions/Actor'
              example: [{"age":23,"fullName":"Sanjana Sanghi Jr","gender":
              "Female","moviesCount":1,"uuid":"32085ed1-5b82-41fc-83b0-7d7650d0b207"}
              ,{"age":52,"fullName":"Sanjana Sanghi","gender":"Female","moviesCount":
              1,"uuid":"2f607b49-771d-4b96-9692-715ea2b38210"}]
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
    pagination = Actor.query.paginate(page, per_page=limit, error_out=False)

    result_dict = {
        'objects': [actor.to_json() for actor in pagination.items],
        'totalCount': pagination.total,
        'totalPages': pagination.pages,
        'page': pagination.page
    }
    if pagination.has_prev:
        result_dict['prevLink'] = url_for(
            'api.get_actors', page=pagination.prev_num)
    if pagination.has_next:
        result_dict['nextLink'] = url_for(
            'api.get_actors', page=pagination.next_num)

    return jsonify(result_dict)


@bp.route('actors/<string:actor_id>')
@auth_required('view:actors')
@cache.memoize(unless=redis_is_not_available)
def get_actor(actor_id):
    """Get a existing Actor.
    The appropriate ``ID`` format must be given, for example: ``2f607b49-771d-4b96-9692-715ea2b38210``
    ---
    tags:
      - actors
    parameters:
      - name: actor_id
        in: path
        description: The `ID` of a existing actor.
        example: 2f607b49-771d-4b96-9692-715ea2b38210
    produces:
      - application/json
    responses:
      200:
        description: A dictionary with the actor attributes.
        schema:
          type: object
          $ref: '#/definitions/Actor'
      401:
        description: if the user is not authenticated.
      403:
        description: If the authenticated user is now allowed to access this 
            resource.
      404:
        description: If the actor ``ID`` does not exist or using an invalid 
            format.
      500:
        description: Something goes wrong within our end.

    """
    actor = None
    try:
        actor = Actor.query.filter_by(uuid=actor_id).first_or_404()
    except StatementError:
        return not_found('please use the correct path parameter')
    return jsonify(actor.to_json())


@bp.route('/actors', methods=['POST'])
@auth_required('add:actors')
def create_actor():
    """Create a new Actor using the submitted attributes.
    All attributes are mandatory.
    ---
    tags:
      - actors
    parameters:
      - name: body
        in: body
        description: The Actor JSON attributes.
        schema:
          properties:
            age:
              type: integer
              description: The age of the Actor.
              required: true
              example: 56
            fullName:
              type: string
              description: The full name of the Actor.
              required: true
              example: "Keanu Reeves"
            gender:
              type: string
              description: The gender of the Actor, could be Female, 
                  Male or Another.
              required: true
              example: "Male"
    consumes:
      - application/json  
    produces:
      - application/json
    responses:
      200:
        description: A dictionary with the actor attributes.
        schema:
          type: object
          $ref: '#/definitions/Actor'
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
    json_actor = request.json or {}
    actor = Actor.new_from_json(json_actor)
    db.session.commit()
    if redis_is_available():
        cache.delete_memoized(get_actors)
    return jsonify(actor.to_json()), 201, \
        {'Location': url_for('api.get_actor', actor_id=str(actor.uuid))}


@bp.route('/actors/<string:actor_id>', methods=['PATCH'])
@auth_required('edit:actors')
def update_actor(actor_id):
    """Update an existing Actor using the the submitted attributes.
    Can update either only the age, the fullName or the gender.
    
    The appropriate ``ID`` format must be given, for example: ``2f607b49-771d-4b96-9692-715ea2b38210``
    ---
    tags:
      - actors
    parameters:
      - name: actor_id
        in: path
        description: The `ID` of a existing actor.
        example: 2f607b49-771d-4b96-9692-715ea2b38210
      - name: body
        in: body
        description: The Actor JSON attributes. Could contain only the age,
            the fullName, the gender, or even all of them.
        schema:
          properties:
            age:
              type: integer
              description: The age of the Actor.
              example: 56
            fullName:
              type: string
              description: The full name of the Actor.
              example: "Keanu Reeves"
            gender:
              type: string
              description: The gender of the Actor, could be Female, 
                  Male or Another.
              example: "Male"
    consumes:
      - application/json  
    produces:
      - application/json
    responses:
      200:
        description: A dictionary with the actor attributes.
        schema:
          type: object
          $ref: '#/definitions/Actor'
      400:
        description: If one of the required parameters were missing, or the movie already.
      401:
        description: If the user is not authenticated.
      403:
        description: if the authenticated user is now allowed to access this 
            resource.
      404:
        description: If the actor ``ID`` does not exist or using an invalid 
            format.
      500:
        description: Something goes wrong within our end.

    """
    actor = None
    try:
        actor = Actor.query.filter_by(uuid=actor_id).first_or_404()
    except StatementError:
        return not_found('please use the correct path parameter')
    json_actor = request.json or {}
    actor.update_from_json(json_actor)
    db.session.commit()
    if redis_is_available():
        cache.delete_memoized(get_actors)
        cache.delete_memoized(get_actor, actor_id)
    return jsonify(actor.to_json())


@bp.route('/actors/<string:actor_id>', methods=['DELETE'])
@auth_required('delete:actors')
def delete_actor(actor_id):
    """Deletes an existing Actor.
    The appropriate ``ID`` format must be given, for example: ``2f607b49-771d-4b96-9692-715ea2b38210``
    ---
    tags:
      - actors
    parameters:
      - name: actor_id
        in: path
        description: The `ID` of a existing actor.
        example: 2f607b49-771d-4b96-9692-715ea2b38210
    responses:
      200:
        description: No content.
      401:
        description: if the user is not authenticated.
      403:
        description: If the authenticated user is now allowed to access this 
            resource.
      404:
        description: If the actor ``ID`` does not exist or using an invalid 
            format.
      500:
        description: Something goes wrong within our end.

    """
    actor = None
    try:
        actor = Actor.query.filter_by(uuid=actor_id).first_or_404()
    except StatementError:
        return not_found('please use the correct path parameter')
    db.session.delete(actor)
    db.session.commit()
    if redis_is_available():
        cache.delete_memoized(get_actors)
        cache.delete_memoized(get_actor, actor_id)
    return '', 204
