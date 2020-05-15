Coffee Shop API Backend
=======================

Udacity has decided to open a new digitally enabled coffee shop where students can order drinks, socialize, and study. But they need help setting up their menu experience.

So Coffee Shop API is the backend application that makes the Coffee Shop Ionic webapp works.

The code follows [PEP 8 style guide](https://pep8.org/).

## Getting Started

### Prerequisites & Installation

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Local Development

#### Database Setup

The SQLite database will be first initialized after the first run of the application. Then the database could be populated with some pre-registered and exported data.

From the `backend` folder run the file `sql_database.sql` into the `database.db` located inside the `database` folder. 

#### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=api.py
export FLASK_ENV=development
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `api.py` directs flask to use the `api.py` file to find the application.

Now run the application

```bash
flask run
```

### Testing

To fully test the API, first import the file `udacity-fsnd-udaspicelatte.postman_collection.json` from the `backend`folder to [Postman](https://www.postman.com/downloads/) and then use the [Collection Runner](https://learning.postman.com/docs/postman/collection-runs/starting-a-collection-run/) to run all tests.

## API Reference

The Coffee Shop API is organized around [REST](http://en.wikipedia.org/wiki/Representational_State_Transfer). The API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, and verbs.

### Base URL

Currently Coffee Shop API is not hosted as a base URL so can only run locally

```
http://127.0.0.1:5000/
```

### Swagger API Reference

After running the server you can check out the complete API Reference by using the Swagger documentation

```
http://127.0.0.1:5000/apidocs
```

### Authentication

The Coffee Shop API uses JSON Web Token (JWT) to authenticate requests.

Users need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H "Authorization: Bearer token`.

### Errors

Coffee Shop API uses conventional HTTP response codes to indicate the success of failure of an API request.

> Codes in the `2xx` range indicate success

> Codes in the `4xx` range indicate an error that failed given the information provided (e.g., a required parameter was omitted)

> Codes in the `5xx` range indicate an error with Bookshelf's servers (you'll rarely see one these)

#### Attributes

Each error contains these attributes:

**code** `integer`

The HTTP code which represents the error occurred.

---

**error** `string`

The identifier which represents the error occurred.

---

**message** `string`

A human-readable message providing more detail about the error.

---

**path** `string`

The relative path of request that originated the error occurred.

---

**success** `boolean`

Will always be `false`.

#### Example

```json
{
  "code": 401,
  "error": "invalid_token",
  "message": "Incorrect token. Please, check the provided token.",
  "path": "/drinks-detail",
  "success": false
}
```

#### Possible errors

| code  | error                 |
|:------|:----------------------|
| 400   | Bad Request           |
| 401   | Unauthorized          |
| 403   | Forbidden             |
| 404   | Resource Not Found    |
| 405   | Method Not Allowed    |
| 500   | Internal Server Error |

### Library

#### Drink

Drink objects represents the main part of the application.

##### Get a list of drinks

Returns a list of Drink with a short form of the recipe.

###### Parameters

No parameters.

###### Returns

A dictionary with the attributes **success** equals to ``true``, a ``list`` of drinks with a short form of the recipe.

###### Request `GET` /drinks

```bash
curl http://127.0.0.1:5000/drinks
```

###### Response

```json
{
  "drinks": [
    {
      "id": 2,
      "recipe": [
        {
          "color": "#9D6947",
          "parts": 1
        },
        {
          "color": "#C8EBFC",
          "parts": 1
        }
      ],
      "title": "Pour-Over Coffee"
    },
    {
      "id": 3,
      "recipe": [
        {
          "color": "#85583C",
          "parts": 1
        },
        {
          "color": "#E4F4FB",
          "parts": 2
        },
        {
          "color": "#EDE1D9",
          "parts": 1
        }
      ],
      "title": "Cafecito"
    },
    {
      "id": 4,
      "recipe": [
        {
          "color": "#BB301B",
          "parts": 2
        },
        {
          "color": "#C3CCF4",
          "parts": 4
        }
      ],
      "title": "The Perfect Cappuccino"
    }
  ],
  "success": true
}
```

##### Get a list of detailed drinks

Returns a list of Drink with a long form of the recipe.

###### Parameters

No parameters.

###### Returns

A dictionary with the attributes **success** equals to ``true``, a ``list`` of drinks with a long form of the recipe.

###### Request `GET` /drinks-detail

```bash
curl http://127.0.0.1:5000/drinks-detail
```

###### Response

```json
{
  "drinks": [
    {
      "id": 2,
      "recipe": [
        {
          "color": "#9D6947",
          "name": "2/3 ounce/18 grams coffee (medium-fine grind)",
          "parts": 1
        },
        {
          "color": "#C8EBFC",
          "name": "10 ounces/300mL filtered, distilled, or spring water",
          "parts": 1
        }
      ],
      "title": "Pour-Over Coffee"
    },
    {
      "id": 3,
      "recipe": [
        {
          "color": "#85583C",
          "name": "1/4 to 1/2 cup coffee (finely ground; or amount needed for pot)",
          "parts": 1
        },
        {
          "color": "#E4F4FB",
          "name": "1 1/2 cups water (or amount for coffee pot)",
          "parts": 2
        },
        {
          "color": "#EDE1D9",
          "name": "1/4 cup white granulated sugar",
          "parts": 1
        }
      ],
      "title": "Cafecito"
    },
    {
      "id": 4,
      "recipe": [
        {
          "color": "#BB301B",
          "name": "2 shots (a double shot)",
          "parts": 2
        },
        {
          "color": "#C3CCF4",
          "name": "4 ounces milk",
          "parts": 4
        }
      ],
      "title": "The Perfect Cappuccino"
    }
  ],
  "success": true
}
```

##### Add a new Drink

Creates a new drink using the submitted title and recipe properties. All of them are mandatory.

###### Parameters

`title` <small>string</small>

The title of the drink. The value must be a `string`.

---

`recipe` <small>array</small>

The full recipe of the drink. The value must be a `array`.

###### Returns

A dictionary with the attributes **success** equals to ``true``, a ``list`` with a single result of the new drink created with a short form of the recipe.

If one of the required parameters were missing this call returns a `400` [error](#Errors).

If the user is not authenticated or is not allowed to access that resource, this call returns either a `401` or `403` [error](#Errors).

If something goes wrong within our end this call returns a `500` [error](#Errors).

###### Request `POST` /drinks

```bash
curl http://127.0.0.1:5000/drinks -X POST -H "Content-Type: application/json" -d '{"recipe":{"color":"brown","name":"grams coffee","parts":1},"title":"Cafe Con Leche"}'
```

###### Response

```json
{
  "drinks": [
    {
      "id": 20,
      "recipe": [
        {
          "color": "brown",
          "parts": 1
        }
      ],
      "title": "Cafe Con Leche"
    }
  ],
  "success": true
}
```

##### Update a single Drink

Updates an existing drink using the submitted title and/or recipe properties. Can update either only the title or only the recipe or both

###### Parameters

`title` <small>string</small>

The title of the drink. The value must be a `string`.

---

`recipe` <small>array</small>

Some attribute of the recipe of the drink. The value must be a `array`.

###### Returns

A dictionary with the attributes **success** equals to ``true``, a ``list`` with a single result of the updated drink with a short form of the recipe.

If all parameters were missing this call returns a `400` [error](#Errors).

If the user is not authenticated or is not allowed to access that resource, this call returns either a `401` or `403` [error](#Errors).

If the question `ID` does not exist, this call returns a `404` [error](#Errors).

If something goes wrong within our end this call returns a `500` [error](#Errors).

###### Request `PATCH` /drinks

```bash
curl http://127.0.0.1:5000/drinks -X PATCH -H "Content-Type: application/json" -d '{"title": "The Perfect Cafe Con Leche"}'
```

###### Response

```json
{
  "drinks": [
    {
      "id": 20,
      "recipe": [
        {
          "color": "brown",
          "parts": 1
        }
      ],
      "title": "The Perfect Cafe Con Leche"
    }
  ],
  "success": true
}
```

##### Delete a single Drink

Deletes an existing drink given `ID` if it exists.

###### Parameters

`ID` <small>integer</small>

A `ID` of a existing drink. The value must be a `integer`.

###### Returns

A dictionary with the attribute **success** equals to ``true`` and attribute **delete** with the ``ID`` of the deleted Drink.

If the user is not authenticated or is not allowed to access that resource, this call returns either a `401` or `403` [error](#Errors).

If the question `ID` does not exist, this call returns a `404` [error](#Errors).

If something goes wrong within our end this call returns a `500` [error](#Errors).

###### Request `DELETE` /drinks

```bash
curl http://127.0.0.1:5000/drinks/20 -X DELETE
```

###### Response

```json
{
  "delete": 20,
  "success": true
}
```

## Authors

- Filipe Bezerra de Sousa (https://about.me/filipebezerra)

## Acknowledgements

- Gabriel Ruttner, one of my program instructor