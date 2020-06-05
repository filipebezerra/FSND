Full Stack Trivia API Backend
=============================

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

So Trivia API is the backend application that makes the Trivia web application works.

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

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

### Local Development

#### Database Setup

With PostgreSQL running, restore a database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

#### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
export FLASK_RUN_HOST=0.0.0.0
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

Setting the `FLASK_RUN_HOST` variable to `0.0.0.0` is optional and will give you remote access to the server.


```bash
export DB_NAME=trivia
export DB_USER=trivia_user
export DB_PASSWORD=trivia_pwd
export DB_HOST=localhost:5432
```

These variables are used by the application to connect to the database running in the PostgreSQL server.

Replace value of the variable `TEST_DB_HOST` with IP address and port if the PostgreSQL server is running on remote.

Now run the application

```bash
flask run
```

### Testing

From within the `backend` directory first ensure you are working using your created virtual environment.

Before running the tests execute

```bash
export TEST_DB_NAME=trivia_test
export TEST_DB_USER=trivia_user
export TEST_DB_PASSWORD=trivia_pwd
export TEST_DB_HOST=localhost:5432
```

These variables are used by test to connect to the database running in the PostgreSQL server.

Replace value of the variable `TEST_DB_HOST` with IP address and port if the PostgreSQL server is running on remote.

To run the tests with `unittest` (with this command you run all existing tests)

```bash
python -m unittest
```

Or just run a specific test

```bash
python test_flaskr.py
```

Sometimes you need to recreate and repopulate the test database. You can use the following script to do that

```bash
./setup_test.sh
```

## API Reference

The Trivia API is organized around [REST](http://en.wikipedia.org/wiki/Representational_State_Transfer). The API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, and verbs.

### Base URL

Currently Trivia API is not hosted as a base URL so can only run locally

```
http://127.0.0.1:5000/api
```

### Swagger API Reference

After running the server you can check out the complete API Reference by using the Swagger documentation

```
http://127.0.0.1:5000/apidocs
```

### Authentication

Currently Trivia API does not require any kind of authentication or API keys.

### Errors

Trivia uses conventional HTTP response codes to indicate the success of failure of an API request.

> Codes in the `2xx` range indicate success

> Codes in the `4xx` range indicate an error that failed given the information provided (e.g., a required parameter was omitted)

> Codes in the `5xx` range indicate an error with Bookshelf's servers (you'll rarely see one these)

#### Attributes

Each request may throw one or many errors:

**errors** `List`

The list of errors occurred within a HTTP request.

Each error contains these attributes:

**code** `integer`

The HTTP code which represents the error occurred.

---

**error** `string`

The name which represents the error occurred.

---

**message** `string`

A human-readable message providing more detail about the error.

---

**path** `string`

The relative path of request that originated the error occurred.

#### Example

```json
{
  "errors": [
    {
      "code": 404,
      "error": "404 Not Found",
      "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
      "path": "/api/questions"
    }
  ]
}
```

#### Possible errors

| code  | error                 |
|:------|:----------------------|
| 400   | Bad Request           |
| 404   | Resource Not Found    |
| 405   | Method Not Allowed    |
| 500   | Internal Server Error |

### Library

#### Category

Category objects represents a way of group books together. Each book has a category attribute which to make the relationship between a book and a category.

##### Get a list of categories

Returns a list of all categories.

###### Parameters

There are no parameters.

###### Returns

A `list` of category objects.

###### Request `GET` /categories

```bash
curl http://127.0.0.1:5000/api/categories
```

###### Response

```json
[
  {
    "id": 1,
    "type": "Science"
  },
  {
    "id": 2,
    "type": "Art"
  },
  {
    "id": 3,
    "type": "Geography"
  }
]
```










#### Question

Question objects represents the main part of the quizzes.

##### Get a list of questions

Returns a list of questions. Can be used with `q` parameter to search for questions or `page` parameter to paginate the result.

###### Parameters

`q` <small>optional</small>

The query term to search for a question.

`page` <small>optional</small>

The page of the result that comes in batches of 10 questions starting from 1. The value must be a `integer`.

###### Returns

A `dictionary` with `categories` property that contains a `list` of all categories. A `questions` property that contains a `list` of paginated questions. A `current_category` property that contains a `integer` of what category was used to filter that result and a `total_questions` counting the total of questions regardless the pagination.

If the given `q` param is empty this call returns a `400` [error](#Errors). If there's no question because of the page submitted, this call returns a `404` [error](#Errors).

###### Request `GET` /questions

```bash
curl http://127.0.0.1:5000/api/questions
```

###### Response

```json
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    }
  ],
  "current_category": 2,
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ],
  "total_questions": 3
}
```

##### Get a list of questions by a category ID

Returns a list of questions filtering by a specific category `ID`. Can be used with `page` parameter to paginate the result.

###### Parameters

`ID` <small>integer</small>

A `ID` of a existing question. The value must be a `integer`.

`page` <small>optional</small>

The page of the result that comes in batches of 10 questions starting from 1. The value must be a `integer`.

###### Returns

A `dictionary` with `categories` property that contains a `list` of all categories. A `questions` property that contains a `list` of paginated questions. A `current_category` property that contains a `integer` of what category was used to filter that result and a `total_questions` counting the total of questions regardless the pagination.

If there's no result for the request, this call returns a `404` [error](#Errors).

###### Request `GET` /categories/1/questions

```bash
curl http://127.0.0.1:5000/api/categories/1/questions
```

###### Response

```json
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    }
  ],
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "total_questions": 3
}
```

##### Add a new question

Creates a new question using the submitted answer, category, difficulty and question properties. All of them are mandatory.

###### Parameters

`answer` <small>string</small>

The answer of the question. The value must be a `string`.

---

`category` <small>integer</small>

The category the question is related of. The value must be a `integer`.

---

`difficulty` <small>integer</small>

The degree of difficulty. The value must be a `integer` between 1 a 5.

---

`question` <small>string</small>

The question itself. The value must be a `string`.

###### Returns

A `dictionary` with the same properties sent in the request additionaly with a `id` property.

If one of the required parameters were missing this call returns a `400` [error](#Errors). If something goes wrong within our end this call returns a `500` [error](#Errors).

###### Request `POST` /questions

```bash
curl http://127.0.0.1:5000/api/questions -X POST -H "Content-Type: application/json" -d '{"answer":"1929", "question":"In which year the Great Depression started in United States?", "category":4, "difficulty": 2}'
```

###### Response

```json
{
  "answer": "1929",
  "category": 4,
  "difficulty": 2,
  "id": 34,
  "question": "In which year the Great Depression started in United States?"
}
```

##### Remove a specific question by ID.

Deletes an existing question given `ID` if it exists.

###### Parameters

`ID` <small>integer</small>

A `ID` of a existing question. The value must be a `integer`.

###### Returns

No content.

If the question `ID` does not exist, this call returns a `404` [error](#Errors). If the question can't be removed or something goes wrong within our end, this call returns a `500` [error](#Errors).

###### Request `DELETE` /questions

```bash
curl http://127.0.0.1:5000/api/questions/29 -X DELETE
```

###### Response

`204` No Content

#### Quiz

##### Get next question of the current quiz

Returns the first or the next question of the quiz.

###### Parameters

`body` <small>body</small>

The quiz JSON attributes.

###### Example

```json
{
  "previous_questions": [
    20,
    21,
    22
  ],
  "quiz_category": {
    "id": 4,
    "type": "History"
  }
}
```

###### Returns

A `dictionary` with `question` property that contains the question for the quiz and  a `quiz_category` that contains the category used to make this quiz.

###### Request `POST` /quizzes

```bash
curl http://127.0.0.1:5000/api/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [5,9,12], "quiz_category": {"id": 4}}'
```

###### Response

```json
{
  "question": {
    "answer": "Scarab",
    "category": 4,
    "difficulty": 4,
    "id": 23,
    "question": "Which dung beetle was worshipped by the ancient Egyptians?"
  },
  "quiz_category": {
    "id": 4,
    "type": "History"
  }
}
```

## Authors

- Filipe Bezerra de Sousa (https://about.me/filipebezerra)

## Acknowledgements

- Mike, my program mentor
- Kerry McCarthy, my program instructor
- Marlon, from student support