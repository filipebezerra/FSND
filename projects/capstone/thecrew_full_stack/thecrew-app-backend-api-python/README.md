TheCrew API Backend
=======================

The TheCrew is a Casting Agency company that is responsible for creating movies and managing and assigning actors to those movies.

So TheCrew API is the backend application that serves and accepts JSON data for our applications and third-party applications.

The code follows [PEP 8 style guide](https://pep8.org/).

## Getting Started

### Prerequisites & Installation

#### Python 3.7.9

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

Our code was built and tested using Python 3.7.9 but is intented to work with newer versions.

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

- [jose](https://python-jose.readthedocs.io/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

- [Flask-Caching](https://flask-caching.readthedocs.io/en/latest/) is a caching extension for Flask, it adds easy cache support to Flask.

- [dynaconf](https://www.dynaconf.com/) is a Configuration Management for Python, is inspired by the [12-factor application guide](https://12factor.net/config).

### Local Development

#### Database Setup

The SQLite database will be first initialized after the first run of the application. Then the database is automatically populated with some pre-registered data.

#### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=thecrew.py
export FLASK_ENV=development
export FLASK_DEBUG=True
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `thecrew.py` directs flask to use the `api.py` file to find the application.

Setting the `FLASK_DEBUG` variable to `True` will enable debugging the application code.

In development mode `Flask` also accepts an `.env` file so you don't ever need to execute some `export` or `set` (dependent of your operation system) to create the needed environment variables. Just create the `.env` file in root of the application (side by side with `thecrew.py` file):

```bash
FLASK_APP=thecrew.py
FLASK_ENV=development
FLASK_DEBUG=True
```

Create the local database and execute the migrations:

```bash
flask deploy
```

Now run the application:

```bash
flask run
```

### Testing

To automatically test the application you can execute `unittest` command to run all unit and integration tests within the application, from the `backend` folder they're inside the `/tests` folder:

```bash
python -m unittest discover -v -s ./tests -p test*.py
```

### Testing the API

You can test the API using the [Postman](https://www.postman.com/downloads/).

The button bellow redirects you to web version of the API documentation, you must create a postman account for you.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/bb9a373a31eaf0c380d7#?env%5BTheCrew%20App%20Heroku%5D=W3sia2V5IjoiaG9zdCIsInZhbHVlIjoiaHR0cHM6Ly90aGVjcmV3LWFwcC5oZXJva3VhcHAuY29tIiwiZW5hYmxlZCI6dHJ1ZX0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0lzSW10cFpDSTZJalp1VkhreVIyVldNRkkyUVhoZloxcGFNR3RrUVNKOS5leUpwYzNNaU9pSm9kSFJ3Y3pvdkwzUm9aUzFqY21WM0xXWnpibVF1ZFhNdVlYVjBhREF1WTI5dEx5SXNJbk4xWWlJNkltNUlZVkpFV2tNeVVtODJVWFp2TW1KdWFqVTRWMjExYTFJeVZVUklaRFJpUUdOc2FXVnVkSE1pTENKaGRXUWlPaUowYUdWamNtVjNMV0Z3YVNJc0ltbGhkQ0k2TVRZd01UQXdOemM0TXl3aVpYaHdJam94TmpBeE1EazBNVGd6TENKaGVuQWlPaUp1U0dGU1JGcERNbEp2TmxGMmJ6SmlibW8xT0ZkdGRXdFNNbFZFU0dRMFlpSXNJbk5qYjNCbElqb2lkbWxsZHpwaFkzUnZjbk1nWVdSa09tRmpkRzl5Y3lCbFpHbDBPbUZqZEc5eWN5QmtaV3hsZEdVNllXTjBiM0p6SUhacFpYYzZiVzkyYVdWeklHRmtaRHB0YjNacFpYTWdaV1JwZERwdGIzWnBaWE1nWkdWc1pYUmxPbTF2ZG1sbGN5SXNJbWQwZVNJNkltTnNhV1Z1ZEMxamNtVmtaVzUwYVdGc2N5SXNJbkJsY20xcGMzTnBiMjV6SWpwYkluWnBaWGM2WVdOMGIzSnpJaXdpWVdSa09tRmpkRzl5Y3lJc0ltVmthWFE2WVdOMGIzSnpJaXdpWkdWc1pYUmxPbUZqZEc5eWN5SXNJblpwWlhjNmJXOTJhV1Z6SWl3aVlXUmtPbTF2ZG1sbGN5SXNJbVZrYVhRNmJXOTJhV1Z6SWl3aVpHVnNaWFJsT20xdmRtbGxjeUpkZlEuSDBEWURyS2tya0pVUDZzVUlKa2lvTEVJcFpfd1NBSVdLVUN0aERoYnlaTHlxSzFmd0ZhTkJ2dlNUZ2tMREdtbmp2OVBONTVFSnQ4akxvQUdKdkcxYWdzak9LQlgzNEFBMEVGYk9oS2I5cHZXMnRtbVl2Q3pHYlN4SVJ3SEprM2pYLTFDT0lQa3loUjltU0ZaNndUTDhWVjBYLVB4RXFTUkhHWms4WlFtM3lib1Z2dVVNalBZTHBZdzhkb0lpTXhPLVBoWG9ULXNudUlfX3RvSWlOS1Y2M00tTHhnckM2Y04tcFFkMmZIREI0OFBuM0JkYlVtYnRnbUYwOGRCU3hscEEtcWFXc1RMUE85V2FEWTJ6MDAyOU92UkR5WHFuVkNndU1sX0Jnc2hTV0xGM0UyRmtxWHQyRlBUNTVaZkN4MzF1T2p2UDl2SVVVVFc1MGNlTTZaazhBIiwiZW5hYmxlZCI6dHJ1ZX1d)

You can also follow along with the published web version of the API documentation. From there you can easily import to your own postman.

<prev><code>
[https://documenter.getpostman.com/view/121249/TVKHTaKr](https://documenter.getpostman.com/view/121249/TVKHTaKr)
</code></prev>

After logging in the application you can "Copy access token to clipboard" from the welcome page and then change the [environment variables](https://learning.postman.com/docs/sending-requests/variables/) within Postman:

- `host`: The API address. For production set the value to `https://thecrew-app.herokuapp.com` or in development set `http://127.0.0.1:5000`
- `token`: The [authentication](#Authentication) required to send requests

Now you have 10 hours to send requests to the API until it gets expired, then you'll need to request another token.

## API Reference

The TheCrew API is organized around [REST](http://en.wikipedia.org/wiki/Representational_State_Transfer). The API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, and verbs.

You can check out our [API Design](https://docs.google.com/spreadsheets/d/1vS6z2x_Kn3N3y6zgd3WIrYpgtDUmE5qAxnwiaXKJ11E/edit?usp=sharing) documentation.

### Base URL

TheCrew API is currently hosted at Heroku under the followig base URL:

<pre><code>https://thecrew-app.herokuapp.com/api/v1</code></pre>

### API Reference

You can check out the complete API Reference by using the Swagger documentation

<prev><code>
[https://thecrew-app.herokuapp.com/apidocs](https://thecrew-app.herokuapp.com/apidocs)
</code></prev>

### Authentication

The TheCrew API uses JSON Web Token (JWT) to authenticate requests.

Users need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H "Authorization: Bearer token`.

### Errors

TheCrew API uses conventional HTTP response codes to indicate the success of failure of an API request.

> Codes in the `2xx` range indicate success

> Codes in the `4xx` range indicate an error that failed given the information provided (e.g., a required parameter was omitted)

> Codes in the `5xx` range indicate an error with Bookshelf's servers (you'll rarely see one these)

#### Attributes

Each error contains these attributes:

**errors** `list`

A list of errors describing one or more errros that occurred. Each error will have a `code`, a `description` and sometimes a `field`.

---

**message** `string`

A human-readable message providing more detail about the error.

---

**path** `string`

The relative path of request that originated the error occurred.

---

**status** `integer`

The HTTP status code.

#### Examples

```json
{
    "errors": [
        {
            "code": "token_expired",
            "description": "Token expired"
        }
    ],
    "message": "Unauthorized",
    "path": "/api/v1/actors/705b913d-7527-498c-99af-1e4c9cb5255b",
    "status": 401
}
```

```json
{
    "errors": [
        {
            "code": "already_exists",
            "description": "actor Sanjana Sanghi Jr already exists",
            "field": "custom"
        }
    ],
    "message": "Validation failed",
    "path": "/api/v1/actors",
    "status": 400
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
| 406   | Not Acceptable        |
| 500   | Internal Server Error |

#### Validation errors

All error objects have resource and field properties so that your client can tell what the problem is. There's also an error code to let you know what is wrong with the field. These are the possible validation error codes:

| code name        | Description |
|:-----------------|:------------|
| `missing_field`  | A required field on a resource has not been set. |
| `invalid`        | The formatting of a field is invalid. |
| `unprocessable`  | The inputs provided were invalid. |
| `already_exists` | Another resource has the same value as this field. |


### Library

#### Actor

Actor objects are assigned to movies.

##### Get a list of actors

Returns a list of Actor.

###### Parameters

No parameters.

###### Returns

A dictionary with a `objects` attribute which is the list of actors and a `page`, `totalCount`, `totalPages` meta attributes.

If the user is not authenticated or is not allowed to access that resource, this call returns either a `401` or `403` [error](#Errors).

If something goes wrong within our end this call returns a `500` [error](#Errors).

###### Request `GET` /actors

```bash
curl --location --request GET 'https://thecrew-app.herokuapp.com/api/v1/actors' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZuVHkyR2VWMFI2QXhfZ1paMGtkQSJ9.eyJpc3MiOiJodHRwczovL3RoZS1jcmV3LWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6Im5IYVJEWkMyUm82UXZvMmJuajU4V211a1IyVURIZDRiQGNsaWVudHMiLCJhdWQiOiJ0aGVjcmV3LWFwaSIsImlhdCI6MTYwMDU1ODMxMSwiZXhwIjoxNjAwNjQ0NzExLCJhenAiOiJuSGFSRFpDMlJvNlF2bzJibmo1OFdtdWtSMlVESGQ0YiIsInNjb3BlIjoidmlldzphY3RvcnMgYWRkOmFjdG9ycyBlZGl0OmFjdG9ycyBkZWxldGU6YWN0b3JzIHZpZXc6bW92aWVzIGFkZDptb3ZpZXMgZWRpdDptb3ZpZXMgZGVsZXRlOm1vdmllcyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwiYWRkOmFjdG9ycyIsImVkaXQ6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsInZpZXc6bW92aWVzIiwiYWRkOm1vdmllcyIsImVkaXQ6bW92aWVzIiwiZGVsZXRlOm1vdmllcyJdfQ.cNCTYF3PPPW6_BtvFQ3PKyKYLplkzCNwJC_xyyNaiMUf90FuDYUMzQU-tryAUHVM0bUAjZYZiRiopuEGDZ87s1fCUSKjy2hvYkkQysU7bjTCl1ORvWW7WvFg8E-8IPemA6Nf8oOpQBKnEUhlQgPKHGDhZ_j-uOiCtv-GMmb6lVXIU5-1ICQfSeH8HqPCueZRSknpTzwsrx3-5XTwqUIC3VhybNLnhgeW0zJ000-3iaZXrCOgzKMJZR63WqWv37z1PxntILroklhCR4d9S4uRQmX7ondZVRndIt_5Fy3IDhyS3hqwW0Dcs-KhHMbxIdxPZ96yGAAVCRPdgnNHHHchZQ'
```

###### Response

```json
{
    "objects": [
        {
            "age": 23,
            "fullName": "Sanjana Sanghi Jr",
            "gender": "Female",
            "moviesCount": 1,
            "uuid": "32085ed1-5b82-41fc-83b0-7d7650d0b207"
        },
        {
            "age": 52,
            "fullName": "Sanjana Sanghi",
            "gender": "Female",
            "moviesCount": 1,
            "uuid": "2f607b49-771d-4b96-9692-715ea2b38210"
        }
    ],
    "page": 1,
    "totalCount": 2,
    "totalPages": 1
}
```

##### Get a specific actor

Returns a specific Actor object.

###### Parameters

`ID` <small>string</small>

A `ID` of a existing actor. The value must be a `string`.

###### Returns

A dictionary with the actor attributes.

If the user is not authenticated or is not allowed to access that resource, this call returns either a `401` or `403` [error](#Errors).

If the actor `ID` does not exist or using an invalid format, this call returns a `404` [error](#Errors).

If something goes wrong within our end this call returns a `500` [error](#Errors).

###### Request `GET` /actors/<ID>

```bash
curl --location --request GET 'https://thecrew-app.herokuapp.com/api/v1/actors/2f607b49-771d-4b96-9692-715ea2b38210' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZuVHkyR2VWMFI2QXhfZ1paMGtkQSJ9.eyJpc3MiOiJodHRwczovL3RoZS1jcmV3LWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6Im5IYVJEWkMyUm82UXZvMmJuajU4V211a1IyVURIZDRiQGNsaWVudHMiLCJhdWQiOiJ0aGVjcmV3LWFwaSIsImlhdCI6MTYwMDU1ODMxMSwiZXhwIjoxNjAwNjQ0NzExLCJhenAiOiJuSGFSRFpDMlJvNlF2bzJibmo1OFdtdWtSMlVESGQ0YiIsInNjb3BlIjoidmlldzphY3RvcnMgYWRkOmFjdG9ycyBlZGl0OmFjdG9ycyBkZWxldGU6YWN0b3JzIHZpZXc6bW92aWVzIGFkZDptb3ZpZXMgZWRpdDptb3ZpZXMgZGVsZXRlOm1vdmllcyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwiYWRkOmFjdG9ycyIsImVkaXQ6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsInZpZXc6bW92aWVzIiwiYWRkOm1vdmllcyIsImVkaXQ6bW92aWVzIiwiZGVsZXRlOm1vdmllcyJdfQ.cNCTYF3PPPW6_BtvFQ3PKyKYLplkzCNwJC_xyyNaiMUf90FuDYUMzQU-tryAUHVM0bUAjZYZiRiopuEGDZ87s1fCUSKjy2hvYkkQysU7bjTCl1ORvWW7WvFg8E-8IPemA6Nf8oOpQBKnEUhlQgPKHGDhZ_j-uOiCtv-GMmb6lVXIU5-1ICQfSeH8HqPCueZRSknpTzwsrx3-5XTwqUIC3VhybNLnhgeW0zJ000-3iaZXrCOgzKMJZR63WqWv37z1PxntILroklhCR4d9S4uRQmX7ondZVRndIt_5Fy3IDhyS3hqwW0Dcs-KhHMbxIdxPZ96yGAAVCRPdgnNHHHchZQ'
```

###### Response

```json
{
    "age": 52,
    "fullName": "Sanjana Sanghi",
    "gender": "Female",
    "moviesCount": 1,
    "uuid": "2f607b49-771d-4b96-9692-715ea2b38210"
}
```

##### Create an Actor

Creates a new Actor using the submitted attributes. All of them are mandatory.

###### Body

`age` <small>integer</small>

The age of the Actor. The value must be a `integer`.

---

`fullName` <small>string</small>

The full name of the Actor. The value must be a `string`.

---

`gender` <small>string</small>

The gender of the Actor, could be one of: Female, Male or Another. The value must be a `string`.

###### Returns

A dictionary with the actor attributes.

If one of the required parameters were missing, or the actor already exists this call returns a `400` [error](#Errors).

If the user is not authenticated or is not allowed to access that resource, this call returns either a `401` or `403` [error](#Errors).

If something goes wrong within our end this call returns a `500` [error](#Errors).

###### Request `POST` /actors

```bash
curl --location --request POST 'https://thecrew-app.herokuapp.com/api/v1/actors' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZuVHkyR2VWMFI2QXhfZ1paMGtkQSJ9.eyJpc3MiOiJodHRwczovL3RoZS1jcmV3LWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6Im5IYVJEWkMyUm82UXZvMmJuajU4V211a1IyVURIZDRiQGNsaWVudHMiLCJhdWQiOiJ0aGVjcmV3LWFwaSIsImlhdCI6MTYwMDU1ODMxMSwiZXhwIjoxNjAwNjQ0NzExLCJhenAiOiJuSGFSRFpDMlJvNlF2bzJibmo1OFdtdWtSMlVESGQ0YiIsInNjb3BlIjoidmlldzphY3RvcnMgYWRkOmFjdG9ycyBlZGl0OmFjdG9ycyBkZWxldGU6YWN0b3JzIHZpZXc6bW92aWVzIGFkZDptb3ZpZXMgZWRpdDptb3ZpZXMgZGVsZXRlOm1vdmllcyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwiYWRkOmFjdG9ycyIsImVkaXQ6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsInZpZXc6bW92aWVzIiwiYWRkOm1vdmllcyIsImVkaXQ6bW92aWVzIiwiZGVsZXRlOm1vdmllcyJdfQ.cNCTYF3PPPW6_BtvFQ3PKyKYLplkzCNwJC_xyyNaiMUf90FuDYUMzQU-tryAUHVM0bUAjZYZiRiopuEGDZ87s1fCUSKjy2hvYkkQysU7bjTCl1ORvWW7WvFg8E-8IPemA6Nf8oOpQBKnEUhlQgPKHGDhZ_j-uOiCtv-GMmb6lVXIU5-1ICQfSeH8HqPCueZRSknpTzwsrx3-5XTwqUIC3VhybNLnhgeW0zJ000-3iaZXrCOgzKMJZR63WqWv37z1PxntILroklhCR4d9S4uRQmX7ondZVRndIt_5Fy3IDhyS3hqwW0Dcs-KhHMbxIdxPZ96yGAAVCRPdgnNHHHchZQ' \
--header 'Content-Type: application/json' \
--data-raw '{
  "age": 56,
  "fullName": "Keanu Reeves",
  "gender": "Male"
}'
```

###### Response

```json
{
    "age": 56,
    "fullName": "Keanu Reeves",
    "gender": "Male",
    "moviesCount": 0,
    "uuid": "8efcce48-7ca0-4541-bb96-5e4d6308db48"
}
```

##### Update a specific Actor

Updates an existing Actor using the submitted age, fullName or gender attributes. Can update either only the age, the fullName or the gender.

###### Parameters

`ID` <small>string</small>

A `ID` of a existing actor. The value must be a `string`.

###### Body

`age` <small>integer</small>

The age of the Actor. The value must be a `integer`.

---

`fullName` <small>string</small>

The full name of the Actor. The value must be a `string`.

---

`gender` <small>string</small>

The gender of the Actor, could be one of: Female, Male or Another. The value must be a `string`.

###### Returns

A dictionary with the actor attributes.

If all attributes were missing this call returns a `400` [error](#Errors).

If the user is not authenticated or is not allowed to access that resource, this call returns either a `401` or `403` [error](#Errors).

If the actor `ID` does not exist or using an invalid format, this call returns a `404` [error](#Errors).

If something goes wrong within our end this call returns a `500` [error](#Errors).

###### Request `PATCH` /actors/<ID>

```bash
curl --location --request PATCH 'https://thecrew-app.herokuapp.com/8efcce48-7ca0-4541-bb96-5e4d6308db48' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZuVHkyR2VWMFI2QXhfZ1paMGtkQSJ9.eyJpc3MiOiJodHRwczovL3RoZS1jcmV3LWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6Im5IYVJEWkMyUm82UXZvMmJuajU4V211a1IyVURIZDRiQGNsaWVudHMiLCJhdWQiOiJ0aGVjcmV3LWFwaSIsImlhdCI6MTYwMDU1ODMxMSwiZXhwIjoxNjAwNjQ0NzExLCJhenAiOiJuSGFSRFpDMlJvNlF2bzJibmo1OFdtdWtSMlVESGQ0YiIsInNjb3BlIjoidmlldzphY3RvcnMgYWRkOmFjdG9ycyBlZGl0OmFjdG9ycyBkZWxldGU6YWN0b3JzIHZpZXc6bW92aWVzIGFkZDptb3ZpZXMgZWRpdDptb3ZpZXMgZGVsZXRlOm1vdmllcyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwiYWRkOmFjdG9ycyIsImVkaXQ6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsInZpZXc6bW92aWVzIiwiYWRkOm1vdmllcyIsImVkaXQ6bW92aWVzIiwiZGVsZXRlOm1vdmllcyJdfQ.cNCTYF3PPPW6_BtvFQ3PKyKYLplkzCNwJC_xyyNaiMUf90FuDYUMzQU-tryAUHVM0bUAjZYZiRiopuEGDZ87s1fCUSKjy2hvYkkQysU7bjTCl1ORvWW7WvFg8E-8IPemA6Nf8oOpQBKnEUhlQgPKHGDhZ_j-uOiCtv-GMmb6lVXIU5-1ICQfSeH8HqPCueZRSknpTzwsrx3-5XTwqUIC3VhybNLnhgeW0zJ000-3iaZXrCOgzKMJZR63WqWv37z1PxntILroklhCR4d9S4uRQmX7ondZVRndIt_5Fy3IDhyS3hqwW0Dcs-KhHMbxIdxPZ96yGAAVCRPdgnNHHHchZQ' \
--header 'Content-Type: application/json' \
--data-raw '{
  "age": 57
}'
```

###### Response

```json
{
    "age": 57,
    "fullName": "Keanu Reeves",
    "gender": "Male",
    "moviesCount": 0,
    "uuid": "8efcce48-7ca0-4541-bb96-5e4d6308db48"
}
```

##### Delete a specific Actor

Deletes an existing Actor given `ID` if it exists.

###### Parameters

`ID` <small>string</small>

A `ID` of a existing actor. The value must be a `string`.

###### Returns

A 204 NO CONTENT http status.

If the user is not authenticated or is not allowed to access that resource, this call returns either a `401` or `403` [error](#Errors).

If the actor `ID` does not exist, this call returns a `404` [error](#Errors).

If something goes wrong within our end this call returns a `500` [error](#Errors).

###### Request `DELETE` /actors

```bash
curl --location --request DELETE 'https://thecrew-app.herokuapp.com/8efcce48-7ca0-4541-bb96-5e4d6308db48' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZuVHkyR2VWMFI2QXhfZ1paMGtkQSJ9.eyJpc3MiOiJodHRwczovL3RoZS1jcmV3LWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6Im5IYVJEWkMyUm82UXZvMmJuajU4V211a1IyVURIZDRiQGNsaWVudHMiLCJhdWQiOiJ0aGVjcmV3LWFwaSIsImlhdCI6MTYwMDU1ODMxMSwiZXhwIjoxNjAwNjQ0NzExLCJhenAiOiJuSGFSRFpDMlJvNlF2bzJibmo1OFdtdWtSMlVESGQ0YiIsInNjb3BlIjoidmlldzphY3RvcnMgYWRkOmFjdG9ycyBlZGl0OmFjdG9ycyBkZWxldGU6YWN0b3JzIHZpZXc6bW92aWVzIGFkZDptb3ZpZXMgZWRpdDptb3ZpZXMgZGVsZXRlOm1vdmllcyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwiYWRkOmFjdG9ycyIsImVkaXQ6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsInZpZXc6bW92aWVzIiwiYWRkOm1vdmllcyIsImVkaXQ6bW92aWVzIiwiZGVsZXRlOm1vdmllcyJdfQ.cNCTYF3PPPW6_BtvFQ3PKyKYLplkzCNwJC_xyyNaiMUf90FuDYUMzQU-tryAUHVM0bUAjZYZiRiopuEGDZ87s1fCUSKjy2hvYkkQysU7bjTCl1ORvWW7WvFg8E-8IPemA6Nf8oOpQBKnEUhlQgPKHGDhZ_j-uOiCtv-GMmb6lVXIU5-1ICQfSeH8HqPCueZRSknpTzwsrx3-5XTwqUIC3VhybNLnhgeW0zJ000-3iaZXrCOgzKMJZR63WqWv37z1PxntILroklhCR4d9S4uRQmX7ondZVRndIt_5Fy3IDhyS3hqwW0Dcs-KhHMbxIdxPZ96yGAAVCRPdgnNHHHchZQ'
```

###### Response

No body response.

#### Movie

Movie objects are created and managed by us.

##### Get a list of movies

Returns a list of Movie.

###### Parameters

No parameters.

###### Returns

A dictionary with a `objects` attribute which is the list of movies and a `page`, `totalCount`, `totalPages` meta attributes.

If the user is not authenticated or is not allowed to access that resource, this call returns either a `401` or `403` [error](#Errors).

If something goes wrong within our end this call returns a `500` [error](#Errors).

###### Request `GET` /movies

```bash
curl --location --request GET 'https://thecrew-app.herokuapp.com/api/v1/movies' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZuVHkyR2VWMFI2QXhfZ1paMGtkQSJ9.eyJpc3MiOiJodHRwczovL3RoZS1jcmV3LWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6Im5IYVJEWkMyUm82UXZvMmJuajU4V211a1IyVURIZDRiQGNsaWVudHMiLCJhdWQiOiJ0aGVjcmV3LWFwaSIsImlhdCI6MTYwMDU1ODMxMSwiZXhwIjoxNjAwNjQ0NzExLCJhenAiOiJuSGFSRFpDMlJvNlF2bzJibmo1OFdtdWtSMlVESGQ0YiIsInNjb3BlIjoidmlldzphY3RvcnMgYWRkOmFjdG9ycyBlZGl0OmFjdG9ycyBkZWxldGU6YWN0b3JzIHZpZXc6bW92aWVzIGFkZDptb3ZpZXMgZWRpdDptb3ZpZXMgZGVsZXRlOm1vdmllcyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwiYWRkOmFjdG9ycyIsImVkaXQ6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsInZpZXc6bW92aWVzIiwiYWRkOm1vdmllcyIsImVkaXQ6bW92aWVzIiwiZGVsZXRlOm1vdmllcyJdfQ.cNCTYF3PPPW6_BtvFQ3PKyKYLplkzCNwJC_xyyNaiMUf90FuDYUMzQU-tryAUHVM0bUAjZYZiRiopuEGDZ87s1fCUSKjy2hvYkkQysU7bjTCl1ORvWW7WvFg8E-8IPemA6Nf8oOpQBKnEUhlQgPKHGDhZ_j-uOiCtv-GMmb6lVXIU5-1ICQfSeH8HqPCueZRSknpTzwsrx3-5XTwqUIC3VhybNLnhgeW0zJ000-3iaZXrCOgzKMJZR63WqWv37z1PxntILroklhCR4d9S4uRQmX7ondZVRndIt_5Fy3IDhyS3hqwW0Dcs-KhHMbxIdxPZ96yGAAVCRPdgnNHHHchZQ'
```

###### Response

```json
{
    "objects": [
        {
            "actors": [
                {
                    "age": 23,
                    "fullName": "Sanjana Sanghi Jr",
                    "gender": "Female",
                    "moviesCount": 1,
                    "uuid": "32085ed1-5b82-41fc-83b0-7d7650d0b207"
                },
                {
                    "age": 52,
                    "fullName": "Sanjana Sanghi",
                    "gender": "Female",
                    "moviesCount": 1,
                    "uuid": "2f607b49-771d-4b96-9692-715ea2b38210"
                }
            ],
            "releaseDate": "2020-10-31",
            "title": "Dil Bechara 2",
            "uuid": "71104e78-cf30-4436-840c-97253874f2e1"
        },
        {
            "actors": [
                {
                    "age": 56,
                    "fullName": "Keanu Reeves",
                    "gender": "Male",
                    "moviesCount": 1,
                    "uuid": "aedc900e-7fe7-4af5-a556-3d606118f3dc"
                },
                {
                    "age": 54,
                    "fullName": "Halle Berry",
                    "gender": "Female",
                    "moviesCount": 1,
                    "uuid": "75005dc2-2b37-423c-815f-04b677737eac"
                },
                {
                    "age": 77,
                    "fullName": "Ian McShane",
                    "gender": "Male",
                    "moviesCount": 1,
                    "uuid": "cb0c1dca-d058-4505-99b6-024c94a522ac"
                },
                {
                    "age": 59,
                    "fullName": "Laurence Fishburne",
                    "gender": "Male",
                    "moviesCount": 1,
                    "uuid": "0609f0f6-dc13-4c35-8bc7-9396ff55739d"
                },
                {
                    "age": 56,
                    "fullName": "Mark Dacascos",
                    "gender": "Male",
                    "moviesCount": 1,
                    "uuid": "cc16790f-2699-4db2-afc7-05c8e34439e6"
                },
                {
                    "age": 35,
                    "fullName": "Asia Kate Dillon",
                    "gender": "Female",
                    "moviesCount": 1,
                    "uuid": "208c4f74-7106-4a0e-96ae-b333815f2efc"
                },
                {
                    "age": 57,
                    "fullName": "Lance Reddick",
                    "gender": "Male",
                    "moviesCount": 1,
                    "uuid": "42ebc19d-0ca1-44ff-b665-ee329d3d9806"
                }
            ],
            "releaseDate": "2019-05-17",
            "title": "John Wick: Chapter 3 - Parabellum",
            "uuid": "941f7036-a3a2-44f0-8eb7-e2b41f3ab59c"
        }
    ],
    "page": 1,
    "totalCount": 2,
    "totalPages": 1
}
```

##### Get a specific movie

Returns a specific Movie object.

###### Parameters

`ID` <small>string</small>

A `ID` of a existing movie. The value must be a `string`.

###### Returns

A dictionary with the movie attributes.

If the user is not authenticated or is not allowed to access that resource, this call returns either a `401` or `403` [error](#Errors).

If the movie `ID` does not exist or using an invalid format, this call returns a `404` [error](#Errors).

If something goes wrong within our end this call returns a `500` [error](#Errors).

###### Request `GET` /movies/<ID>

```bash
curl --location --request GET 'https://thecrew-app.herokuapp.com/api/v1/movies/003da5c2-2b66-40db-9e41-214e274363e6' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZuVHkyR2VWMFI2QXhfZ1paMGtkQSJ9.eyJpc3MiOiJodHRwczovL3RoZS1jcmV3LWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6Im5IYVJEWkMyUm82UXZvMmJuajU4V211a1IyVURIZDRiQGNsaWVudHMiLCJhdWQiOiJ0aGVjcmV3LWFwaSIsImlhdCI6MTYwMDU1ODMxMSwiZXhwIjoxNjAwNjQ0NzExLCJhenAiOiJuSGFSRFpDMlJvNlF2bzJibmo1OFdtdWtSMlVESGQ0YiIsInNjb3BlIjoidmlldzphY3RvcnMgYWRkOmFjdG9ycyBlZGl0OmFjdG9ycyBkZWxldGU6YWN0b3JzIHZpZXc6bW92aWVzIGFkZDptb3ZpZXMgZWRpdDptb3ZpZXMgZGVsZXRlOm1vdmllcyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwiYWRkOmFjdG9ycyIsImVkaXQ6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsInZpZXc6bW92aWVzIiwiYWRkOm1vdmllcyIsImVkaXQ6bW92aWVzIiwiZGVsZXRlOm1vdmllcyJdfQ.cNCTYF3PPPW6_BtvFQ3PKyKYLplkzCNwJC_xyyNaiMUf90FuDYUMzQU-tryAUHVM0bUAjZYZiRiopuEGDZ87s1fCUSKjy2hvYkkQysU7bjTCl1ORvWW7WvFg8E-8IPemA6Nf8oOpQBKnEUhlQgPKHGDhZ_j-uOiCtv-GMmb6lVXIU5-1ICQfSeH8HqPCueZRSknpTzwsrx3-5XTwqUIC3VhybNLnhgeW0zJ000-3iaZXrCOgzKMJZR63WqWv37z1PxntILroklhCR4d9S4uRQmX7ondZVRndIt_5Fy3IDhyS3hqwW0Dcs-KhHMbxIdxPZ96yGAAVCRPdgnNHHHchZQ'
```

###### Response

```json
{
    "actors": [
        {
            "age": 56,
            "fullName": "Keanu Reeves",
            "gender": "Male",
            "moviesCount": 1,
            "uuid": "aedc900e-7fe7-4af5-a556-3d606118f3dc"
        },
        {
            "age": 54,
            "fullName": "Halle Berry",
            "gender": "Female",
            "moviesCount": 1,
            "uuid": "75005dc2-2b37-423c-815f-04b677737eac"
        },
        {
            "age": 77,
            "fullName": "Ian McShane",
            "gender": "Male",
            "moviesCount": 1,
            "uuid": "cb0c1dca-d058-4505-99b6-024c94a522ac"
        },
        {
            "age": 59,
            "fullName": "Laurence Fishburne",
            "gender": "Male",
            "moviesCount": 1,
            "uuid": "0609f0f6-dc13-4c35-8bc7-9396ff55739d"
        },
        {
            "age": 56,
            "fullName": "Mark Dacascos",
            "gender": "Male",
            "moviesCount": 1,
            "uuid": "cc16790f-2699-4db2-afc7-05c8e34439e6"
        },
        {
            "age": 35,
            "fullName": "Asia Kate Dillon",
            "gender": "Female",
            "moviesCount": 1,
            "uuid": "208c4f74-7106-4a0e-96ae-b333815f2efc"
        },
        {
            "age": 57,
            "fullName": "Lance Reddick",
            "gender": "Male",
            "moviesCount": 1,
            "uuid": "42ebc19d-0ca1-44ff-b665-ee329d3d9806"
        }
    ],
    "releaseDate": "2019-05-17",
    "title": "John Wick: Chapter 3 - Parabellum",
    "uuid": "941f7036-a3a2-44f0-8eb7-e2b41f3ab59c"
}
```

##### Create an Movie

Creates a new Movie using the submitted attributes. All of them are mandatory.

###### Body

`title` <small>string</small>

The title of the Movie. The value must be a `string`.

---

`releaseDate` <small>string</small>

The date when the Movie was release. The value must be a `string`.

---

`actors` <small>list</small>

A list of objects containing at least the `uuid` of each Actor.

###### Returns

A dictionary with the movie attributes.

If one of the required parameters were missing, or the movie already exists this call returns a `400` [error](#Errors).

If the user is not authenticated or is not allowed to access that resource, this call returns either a `401` or `403` [error](#Errors).

If something goes wrong within our end this call returns a `500` [error](#Errors).

###### Request `POST` /movies

```bash
curl --location --request POST 'https://thecrew-app.herokuapp.com/api/v1/movies' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZuVHkyR2VWMFI2QXhfZ1paMGtkQSJ9.eyJpc3MiOiJodHRwczovL3RoZS1jcmV3LWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6Im5IYVJEWkMyUm82UXZvMmJuajU4V211a1IyVURIZDRiQGNsaWVudHMiLCJhdWQiOiJ0aGVjcmV3LWFwaSIsImlhdCI6MTYwMDU1ODMxMSwiZXhwIjoxNjAwNjQ0NzExLCJhenAiOiJuSGFSRFpDMlJvNlF2bzJibmo1OFdtdWtSMlVESGQ0YiIsInNjb3BlIjoidmlldzphY3RvcnMgYWRkOmFjdG9ycyBlZGl0OmFjdG9ycyBkZWxldGU6YWN0b3JzIHZpZXc6bW92aWVzIGFkZDptb3ZpZXMgZWRpdDptb3ZpZXMgZGVsZXRlOm1vdmllcyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwiYWRkOmFjdG9ycyIsImVkaXQ6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsInZpZXc6bW92aWVzIiwiYWRkOm1vdmllcyIsImVkaXQ6bW92aWVzIiwiZGVsZXRlOm1vdmllcyJdfQ.cNCTYF3PPPW6_BtvFQ3PKyKYLplkzCNwJC_xyyNaiMUf90FuDYUMzQU-tryAUHVM0bUAjZYZiRiopuEGDZ87s1fCUSKjy2hvYkkQysU7bjTCl1ORvWW7WvFg8E-8IPemA6Nf8oOpQBKnEUhlQgPKHGDhZ_j-uOiCtv-GMmb6lVXIU5-1ICQfSeH8HqPCueZRSknpTzwsrx3-5XTwqUIC3VhybNLnhgeW0zJ000-3iaZXrCOgzKMJZR63WqWv37z1PxntILroklhCR4d9S4uRQmX7ondZVRndIt_5Fy3IDhyS3hqwW0Dcs-KhHMbxIdxPZ96yGAAVCRPdgnNHHHchZQ' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "John Wick: Chapter 3 - Parabellum",
    "releaseDate": "2019-05-17",
    "actors": [
        {
            "uuid": "aedc900e-7fe7-4af5-a556-3d606118f3dc"
        },
        {
            "uuid": "75005dc2-2b37-423c-815f-04b677737eac"
        },
        {
            "uuid": "cb0c1dca-d058-4505-99b6-024c94a522ac"
        },
        {
            "uuid": "0609f0f6-dc13-4c35-8bc7-9396ff55739d"
        },
        {
            "uuid": "cc16790f-2699-4db2-afc7-05c8e34439e6"
        },
        {
            "uuid": "208c4f74-7106-4a0e-96ae-b333815f2efc"
        },
        {
            "uuid": "42ebc19d-0ca1-44ff-b665-ee329d3d9806"
        }
    ]
}'
```

###### Response

```json
{
    "actors": [
        {
            "age": 56,
            "fullName": "Keanu Reeves",
            "gender": "Male",
            "moviesCount": 1,
            "uuid": "aedc900e-7fe7-4af5-a556-3d606118f3dc"
        },
        {
            "age": 54,
            "fullName": "Halle Berry",
            "gender": "Female",
            "moviesCount": 1,
            "uuid": "75005dc2-2b37-423c-815f-04b677737eac"
        },
        {
            "age": 77,
            "fullName": "Ian McShane",
            "gender": "Male",
            "moviesCount": 1,
            "uuid": "cb0c1dca-d058-4505-99b6-024c94a522ac"
        },
        {
            "age": 59,
            "fullName": "Laurence Fishburne",
            "gender": "Male",
            "moviesCount": 1,
            "uuid": "0609f0f6-dc13-4c35-8bc7-9396ff55739d"
        },
        {
            "age": 56,
            "fullName": "Mark Dacascos",
            "gender": "Male",
            "moviesCount": 1,
            "uuid": "cc16790f-2699-4db2-afc7-05c8e34439e6"
        },
        {
            "age": 35,
            "fullName": "Asia Kate Dillon",
            "gender": "Female",
            "moviesCount": 1,
            "uuid": "208c4f74-7106-4a0e-96ae-b333815f2efc"
        },
        {
            "age": 57,
            "fullName": "Lance Reddick",
            "gender": "Male",
            "moviesCount": 1,
            "uuid": "42ebc19d-0ca1-44ff-b665-ee329d3d9806"
        }
    ],
    "releaseDate": "2019-05-17",
    "title": "John Wick: Chapter 3 - Parabellum",
    "uuid": "941f7036-a3a2-44f0-8eb7-e2b41f3ab59c"
}
```

##### Update a specific Movie

Updates an existing Movie using the submitted title, releaseDate or actors attributes. Can update either only the title, the releaseDate or the actors.

###### Parameters

`ID` <small>string</small>

A `ID` of a existing movie. The value must be a `string`.

###### Body

`title` <small>string</small>

The title of the Movie. The value must be a `string`.

---

`releaseDate` <small>string</small>

The date when the Movie was release. The value must be a `string`.

---

`actors` <small>list</small>

A list of objects containing at least the `uuid` of each Actor.

###### Returns

A dictionary with the movie attributes.

If all attributes were missing, or the movie already exists this call returns a `400` [error](#Errors).

If the user is not authenticated or is not allowed to access that resource, this call returns either a `401` or `403` [error](#Errors).

If the actor `ID` does not exist or using an invalid format, this call returns a `404` [error](#Errors).

If something goes wrong within our end this call returns a `500` [error](#Errors).

###### Request `PATCH` /movies/<ID>

```bash
curl --location --request PATCH 'https://thecrew-app.herokuapp.com/api/v1/movies/941f7036-a3a2-44f0-8eb7-e2b41f3ab59c' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZuVHkyR2VWMFI2QXhfZ1paMGtkQSJ9.eyJpc3MiOiJodHRwczovL3RoZS1jcmV3LWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6Im5IYVJEWkMyUm82UXZvMmJuajU4V211a1IyVURIZDRiQGNsaWVudHMiLCJhdWQiOiJ0aGVjcmV3LWFwaSIsImlhdCI6MTYwMDU1ODMxMSwiZXhwIjoxNjAwNjQ0NzExLCJhenAiOiJuSGFSRFpDMlJvNlF2bzJibmo1OFdtdWtSMlVESGQ0YiIsInNjb3BlIjoidmlldzphY3RvcnMgYWRkOmFjdG9ycyBlZGl0OmFjdG9ycyBkZWxldGU6YWN0b3JzIHZpZXc6bW92aWVzIGFkZDptb3ZpZXMgZWRpdDptb3ZpZXMgZGVsZXRlOm1vdmllcyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwiYWRkOmFjdG9ycyIsImVkaXQ6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsInZpZXc6bW92aWVzIiwiYWRkOm1vdmllcyIsImVkaXQ6bW92aWVzIiwiZGVsZXRlOm1vdmllcyJdfQ.cNCTYF3PPPW6_BtvFQ3PKyKYLplkzCNwJC_xyyNaiMUf90FuDYUMzQU-tryAUHVM0bUAjZYZiRiopuEGDZ87s1fCUSKjy2hvYkkQysU7bjTCl1ORvWW7WvFg8E-8IPemA6Nf8oOpQBKnEUhlQgPKHGDhZ_j-uOiCtv-GMmb6lVXIU5-1ICQfSeH8HqPCueZRSknpTzwsrx3-5XTwqUIC3VhybNLnhgeW0zJ000-3iaZXrCOgzKMJZR63WqWv37z1PxntILroklhCR4d9S4uRQmX7ondZVRndIt_5Fy3IDhyS3hqwW0Dcs-KhHMbxIdxPZ96yGAAVCRPdgnNHHHchZQ' \
--header 'Content-Type: application/json' \
--data-raw '{
  "releaseDate": "2019-05-19"
}'
```

###### Response

```json
{
    "actors": [
        {
            "age": 56,
            "fullName": "Keanu Reeves",
            "gender": "Male",
            "moviesCount": 1,
            "uuid": "aedc900e-7fe7-4af5-a556-3d606118f3dc"
        },
        {
            "age": 54,
            "fullName": "Halle Berry",
            "gender": "Female",
            "moviesCount": 1,
            "uuid": "75005dc2-2b37-423c-815f-04b677737eac"
        },
        {
            "age": 77,
            "fullName": "Ian McShane",
            "gender": "Male",
            "moviesCount": 1,
            "uuid": "cb0c1dca-d058-4505-99b6-024c94a522ac"
        },
        {
            "age": 59,
            "fullName": "Laurence Fishburne",
            "gender": "Male",
            "moviesCount": 1,
            "uuid": "0609f0f6-dc13-4c35-8bc7-9396ff55739d"
        },
        {
            "age": 56,
            "fullName": "Mark Dacascos",
            "gender": "Male",
            "moviesCount": 1,
            "uuid": "cc16790f-2699-4db2-afc7-05c8e34439e6"
        },
        {
            "age": 35,
            "fullName": "Asia Kate Dillon",
            "gender": "Female",
            "moviesCount": 1,
            "uuid": "208c4f74-7106-4a0e-96ae-b333815f2efc"
        },
        {
            "age": 57,
            "fullName": "Lance Reddick",
            "gender": "Male",
            "moviesCount": 1,
            "uuid": "42ebc19d-0ca1-44ff-b665-ee329d3d9806"
        }
    ],
    "releaseDate": "2019-05-19",
    "title": "John Wick: Chapter 3 - Parabellum",
    "uuid": "941f7036-a3a2-44f0-8eb7-e2b41f3ab59c"
}
```

##### Delete a specific Movie

Deletes an existing Movie given `ID` if it exists.

###### Parameters

`ID` <small>string</small>

A `ID` of a existing movie. The value must be a `string`.

###### Returns

A 204 NO CONTENT http status.

If the user is not authenticated or is not allowed to access that resource, this call returns either a `401` or `403` [error](#Errors).

If the movie `ID` does not exist or using an invalid format, this call returns a `404` [error](#Errors).

If something goes wrong within our end this call returns a `500` [error](#Errors).

###### Request `DELETE` /movies

```bash
curl --location --request DELETE 'https://thecrew-app.herokuapp.com/api/v1/movies/941f7036-a3a2-44f0-8eb7-e2b41f3ab59c' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZuVHkyR2VWMFI2QXhfZ1paMGtkQSJ9.eyJpc3MiOiJodHRwczovL3RoZS1jcmV3LWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6Im5IYVJEWkMyUm82UXZvMmJuajU4V211a1IyVURIZDRiQGNsaWVudHMiLCJhdWQiOiJ0aGVjcmV3LWFwaSIsImlhdCI6MTYwMDU1ODMxMSwiZXhwIjoxNjAwNjQ0NzExLCJhenAiOiJuSGFSRFpDMlJvNlF2bzJibmo1OFdtdWtSMlVESGQ0YiIsInNjb3BlIjoidmlldzphY3RvcnMgYWRkOmFjdG9ycyBlZGl0OmFjdG9ycyBkZWxldGU6YWN0b3JzIHZpZXc6bW92aWVzIGFkZDptb3ZpZXMgZWRpdDptb3ZpZXMgZGVsZXRlOm1vdmllcyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwiYWRkOmFjdG9ycyIsImVkaXQ6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsInZpZXc6bW92aWVzIiwiYWRkOm1vdmllcyIsImVkaXQ6bW92aWVzIiwiZGVsZXRlOm1vdmllcyJdfQ.cNCTYF3PPPW6_BtvFQ3PKyKYLplkzCNwJC_xyyNaiMUf90FuDYUMzQU-tryAUHVM0bUAjZYZiRiopuEGDZ87s1fCUSKjy2hvYkkQysU7bjTCl1ORvWW7WvFg8E-8IPemA6Nf8oOpQBKnEUhlQgPKHGDhZ_j-uOiCtv-GMmb6lVXIU5-1ICQfSeH8HqPCueZRSknpTzwsrx3-5XTwqUIC3VhybNLnhgeW0zJ000-3iaZXrCOgzKMJZR63WqWv37z1PxntILroklhCR4d9S4uRQmX7ondZVRndIt_5Fy3IDhyS3hqwW0Dcs-KhHMbxIdxPZ96yGAAVCRPdgnNHHHchZQ'
```

###### Response

No body response.


## Authors

- Filipe Bezerra de Sousa (https://about.me/filipebezerra)

## Acknowledgements

- Amy Hua, one of my program instructor
- Kerry McCarthy, one of my program instructor
- Gabriel Ruttner, one of my program instructor
- Kennedy Behrman, one of my program instructor