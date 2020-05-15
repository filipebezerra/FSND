"""
    api.py
    -------

    This module contains the RESTful API responsible for getting, creating,
    updating and deleting drink resources.
"""

__author__ = "Filipe Bezerra de Sousa"

import logging

from flasgger import Swagger
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from jsonpatch import JsonPatchException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from werkzeug.exceptions import HTTPException

from .auth.auth import AuthError, requires_auth
from .database.data_manager import DrinkDataManager
from .database.models import setup_db

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/*": {"origins": "*"}})
swagger = Swagger(app)
logging.basicConfig(filename="api.log", level=logging.ERROR)


@app.after_request
def after_request(response):
    """Modify response headers including Access-Control-* headers.

    :param response: An instance of the response object.
    :return: As instance of the response object with Access-Control-* headers.
    """
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type, Authorization"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
    )
    return response


@app.route("/drinks")
def get_drinks():
    """Get a list of Drink with a short form of the recipe.
    ---
    tags:
      - drinks
    definitions:
      Recipe:
        type: object
        properties:
          color:
            type: string
            example: brown
          name:
            type: string
            example: grams coffee
          parts:
            type: integer
            example: 1
      Drink:
        type: object
        properties:
          id:
            type: integer
            example: 1
          title:
            type: string
            example: Cafecito
          recipe:
            type: array
            $ref: '#/definitions/Recipe'
    produces:
      - application/json
    responses:
      200:
        description: A dictionary with the attributes **success** equals to
            ``true``, a ``list`` of drinks with a short form of the recipe.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            drinks:
              type: array
              items:
                $ref: '#/definitions/Drink'
              example: [{"id":2,"recipe":[{"color":"#9D6947","parts":1},
              {"color":"#C8EBFC","parts":1}],"title":"Pour-Over Coffee"}]

    """
    drinks = DrinkDataManager.list_drinks(False)
    return jsonify({"success": True, "drinks": drinks,})


@app.route("/drinks-detail")
@requires_auth("get:drinks-detail")
def get_drinks_detail(payload):
    """Get a list of Drink with a long form of the recipe.
    ---
    tags:
      - drinks
    produces:
      - application/json
    responses:
      403:
        description: If the authenticated user is now allowed to access this
            resource.
      401:
        description: If the user is not authenticated.
      400:
        description: If the authorization token is not valid.
      200:
        description: A dictionary with the attributes **success** equals to
            ``true``, a ``list`` of drinks with a long form of the recipe.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            drinks:
              type: array
              items:
                $ref: '#/definitions/Drink'
              example: [{"id":2,"recipe":[{"color":"#9D6947",
              "name":"2/3 ounce/18 grams coffee (medium-fine grind)",
              "parts":1},{"color":"#C8EBFC","name":"10 ounces/300mL filtered,
              distilled, or spring water","parts":1}],
              "title":"Pour-Over Coffee"}]

    """
    drinks = DrinkDataManager.list_drinks()
    return jsonify({"success": True, "drinks": drinks,})


@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def post_drink(payload):
    """Add a new Drink.
    ---
    tags:
      - drinks
    parameters:
      - name: body
        in: body
        description: The Drink JSON attributes.
        schema:
          properties:
            title:
              type: string
              description: The title of the drink.
              required: true
              example: Cafe Con Leche
            recipe:
              type: array
              description: The full recipe of the drink.
              required: true
              $ref: '#/definitions/Recipe'
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      500:
        description: If something goes wrong within our end.
      403:
        description: If the authenticated user is now allowed to access this
            resource.
      401:
        description: If the user is not authenticated.
      400:
        description: If the authorization token is not valid or if the drink
            title is already took.
      200:
        description: A dictionary with the attributes **success** equals to
            ``true``, a ``list`` with a single result of the new drink created
            with a short form of the recipe.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            drinks:
              type: array
              items:
                $ref: '#/definitions/Drink'
              example: [{"id":20,"recipe":[{"color":"brown","parts":1}],
              "title":"Cafe Con Leche"}]

    """
    body = request.get_json()

    recipe = body.get("recipe")

    if (
            not all([body.get("title"), recipe])
            or not isinstance(recipe, list)
            or not all(
                all([item.get("color"), item.get("name"), item.get("parts")])
                for item in recipe
            )
    ):
        abort(400, description="All fields are required.")

    try:
        drink = DrinkDataManager.create_drink(body)
        return jsonify({"success": True, "drinks": [drink],})
    except IntegrityError:
        abort(400, "The drink title is already took.")
    except SQLAlchemyError as exc:
        app.logger.error(str(exc))
        abort(500)


@app.route("/drinks/<int:drink_id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def patch_drink(payload, drink_id):
    """Update a single Drink. Can update either only the title or only the
    recipe or both.
    ---
    tags:
      - drinks
    parameters:
      - name: drink_id
        in: path
        description: The ID of the Drink to be updated.
        example: 20
      - name: body
        in: body
        description: The Drink JSON attributes. Could contain only the title
            or the recipe, or even both.
        schema:
          properties:
            title:
              type: string
              description: The title of the drink.
              example: The Perfect Cafe Con Leche
            recipe:
              type: array
              description: A single attribute of even the full recipe of the
                    drink.
              $ref: '#/definitions/Recipe'
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      500:
        description: If something goes wrong within our end.
      404:
        description: If the given ID doesn't exists.
      403:
        description: If the authenticated user is now allowed to access this
            resource.
      401:
        description: If the user is not authenticated.
      400:
        description: If the authorization token is not valid or if the drink
            title is already took.
      200:
        description: A dictionary with the attributes **success** equals to
            ``true``, a ``list`` with a single result of the updated drink
            with a short form of the recipe.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            drinks:
              type: array
              items:
                $ref: '#/definitions/Drink'
              example: [{"id":20,"recipe":[{"color":"brown","parts":1}],
              "title":"The Perfect Cafe Con Leche"}]

    """
    body = request.get_json()

    if not any([body.get("title"), body.get("recipe")]) or (
            "recipe" in body
            and not (
                isinstance(body["recipe"], list)
                and all(
                    any([item["color"], item["name"], item["parts"]])
                    for item in body["recipe"]
                )
            )
    ):
        abort(
            400,
            description='You must specify either the "title" or '
            '"all recipe attributes".',
        )

    try:
        drink = DrinkDataManager.update_drink(drink_id, body)
        return jsonify({"success": True, "drinks": [drink],})
    except IntegrityError:
        abort(400, "The drink title is already took.")
    except (SQLAlchemyError, JsonPatchException) as exc:
        app.logger.error(str(exc))
        abort(500)


@app.route("/drinks/<int:drink_id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(payload, drink_id):
    """Delete a single Drink.
    ---
    tags:
      - drinks
    parameters:
      - name: drink_id
        in: path
        description: The ID of the Drink to be deleted.
        example: 20
    produces:
      - application/json
    responses:
      500:
        description: If something goes wrong within our end.
      404:
        description: If the given ID doesn't exists.
      403:
        description: If the authenticated user is now allowed to access this
            resource.
      401:
        description: If the user is not authenticated.
      400:
        description: If the authorization token is not valid.
      200:
        description: A dictionary with the attribute **success** equals to
            ``true`` and attribute **delete** with the ``ID`` of the deleted
            Drink.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            delete:
              type: integer
              example: 20

    """
    try:
        DrinkDataManager.delete_drink(drink_id)
        return jsonify({"success": True, "delete": drink_id})
    except SQLAlchemyError as exc:
        app.logger.error(str(exc))
        abort(500)


@app.errorhandler(HTTPException)
def handle_http_exception(exception):
    """Handle any HTTP error when handling any HTTP request.

    :param exception: The HTTP exception.
    :return: A JSON-formatted error.
    """
    error_name = exception.name.lower().replace(" ", "_")
    return handle_error(exception.code, error_name, exception.description)


@app.errorhandler(AuthError)
def handle_auth_error(exception):
    """Handle a :class:`AuthError` error when an HTTP request tries to access
    a resource which needs a authenticated user with the required permission.

    :param exception: The auth exception.
    :return: A JSON-formatted error.
    """
    return handle_error(
        exception.status_code,
        exception.error["code"],
        exception.error["description"],
    )


def handle_error(error_code, error_name, error_description):
    """A convenient helper function to convert an exception to an
    JSON-formatted error.

    :param error_code: The HTTP code which represents the error occurred.
    :param error_name: The identifier which represents the error occurred.
    :param error_description: A human-readable message providing more detail
     about the error.
    :return: A JSON-formatted error.
    """
    return (
        jsonify(
            {
                "success": False,
                "code": error_code,
                "error": error_name,
                "message": error_description,
                "path": request.path,
            }
        ),
        error_code,
    )


if __name__ == "__main__":
    app.run(
        debug=True,
        use_debugger=False,
        use_reloader=False,
        passthrough_errors=True,
    )
