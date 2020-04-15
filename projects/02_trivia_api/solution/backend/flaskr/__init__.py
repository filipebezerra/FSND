from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from sqlalchemy import exc
from werkzeug.exceptions import HTTPException, default_exceptions, _aborter
from flasgger import Swagger

from models import setup_db, Question, Category


class NoContent(HTTPException):
    """*204* `No Content`

    `HttpException` that results HTTP status code 204 - No Content.

    Attributes:
        code (int) : HTTP status code.
        description (str) : HTTP error description.

    """

    code = 204
    description = "The server successfully processed the request, "\
                  "but is not returning any content."


default_exceptions[204] = NoContent
_aborter.mapping[204] = NoContent

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    """Create and configure the app.

    Args:
        test_config (dict) : Used in a testing environment.

    Returns:
       Flask instance application.

    """
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    swagger = Swagger(app)

    @app.after_request
    def after_request(response):
        """Modify response headers including Access-Control-* headers.

        Args:
            response (~werkzeug.wrappers.Response) : An instance of the response object.

        Returns:
            response (~werkzeug.wrappers.Response) : As instance of the response object with Access-Control-* headers.

        """
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS"
        )
        return response

    @app.route("/api/questions")
    def get_questions():
        """Get a list of questions.
        Can be used with a ``q`` parameter to search for questions or ``page`` parameter to paginate the result.
        ---
        tags:
          - questions
        parameters:
          - name: q
            in: query
            type: string
            required: false
            description: The query term to search for a question.
          - name: page
            in: query
            type: integer
            required: false
            description: The page of the result that comes in batches of 10 questions.
            default: 1
        definitions:
          Category:
            type: object
            properties:
              id:
                type: integer
                example: 4
              type:
                type: string
                example: History
          Question:
            type: object
            properties:
              answer:
                type: string
                example: Maya Angelou
              category:
                type: integer
                example: 4
              difficulty:
                type: integer
                example: 2
              id:
                type: integer
                example: 5
              question:
                type: string
                example: Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?
        produces:
          - application/json
        responses:
          400:
            description: If the given `q` param is empty.
          404:
            description: If there's no result for the request.
          200:
            description: A dictionary containing a list of questions, a list of categories, the current category and\
            the total of questions regardless the pagination.
            schema:
              type: object
              properties:
                categories:
                  type: array
                  items:
                    $ref: '#/definitions/Category'
                  example: [{"id":1,"type":"Science"},{"id":2,"type":"Art"},{"id":3,"type":"Geography"}]
                current_category:
                  type: integer
                  example: 2
                questions:
                  type: array
                  items:
                    $ref: '#/definitions/Question'
                  example: [{"answer":"Escher","category":2,"difficulty":1,"id":16,"question":\
                  "Which Dutch graphic artist–initials M C was a creator of optical illusions?"},\
                  {"answer":"Mona Lisa","category":2,"difficulty":3,"id":17,"question":\
                  "La Giaconda is better known as what?"}]
                total_questions:
                  type: integer
                  example: 2

        """
        if request.args and "q" in request.args:
            return get_questions_for_query_term()
        else:
            first_category = Category.query.order_by(
                Category.type.asc()
            ).first()
            return get_questions_for_category(first_category.id)

    @app.route("/api/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):
        """Get a list of questions by a category ID.
        Can be used with a ``page`` parameter to paginate the result.
        ---
        tags:
          - questions
        parameters:
          - name: category_id
            in: path
            type: integer
            required: true
            description: The ID of the specific category which questions are related to.
          - name: page
            in: query
            type: integer
            required: false
            description: The page of the result that comes in batches of 10 questions.
            default: 1
        produces:
          - application/json
        responses:
          404:
            description: If there's no result for the request.
          200:
            description: A dictionary containing a list of questions, a list of categories, the current category and\
            the total of questions regardless the pagination.
            schema:
              type: object
              properties:
                categories:
                  type: array
                  items:
                    $ref: '#/definitions/Category'
                  example: [{"id":1,"type":"Science"},{"id":2,"type":"Art"},{"id":3,"type":"Geography"}]
                current_category:
                  type: integer
                  example: 2
                questions:
                  type: array
                  items:
                    $ref: '#/definitions/Question'
                  example: [{"answer":"Escher","category":2,"difficulty":1,"id":16,"question":\
                  "Which Dutch graphic artist–initials M C was a creator of optical illusions?"},\
                  {"answer":"Mona Lisa","category":2,"difficulty":3,"id":17,"question":\
                  "La Giaconda is better known as what?"}]
                total_questions:
                  type: integer
                  example: 2

        """
        return get_questions_for_category(category_id)

    def get_questions_for_category(category_id):
        """Retrieve a list of questions filtered by the ID of the category.

        Also the result will be paginated using the default page of 1 if the query parameter ``page`` were omitted.

        Args:
            category_id (int) : The ID of the specific category which questions are related to.

        Returns:
            A dictionary containing a list of questions, a list of categories, the current category and the\
            total of questions regardless the pagination.

        Raises:
            HTTPException(404): If there's no result for the default or specified page.

        """
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        selection = Question.query.filter_by(category=str(category_id)).all()
        result_questions = [q.format() for q in selection][start:end]

        if not len(result_questions):
            return abort(404)

        return jsonify(
            {
                "questions": result_questions,
                "total_questions": len(selection),
                "current_category": category_id,
                "categories": query_all_categories(),
            }
        )

    def get_questions_for_query_term():
        """Retrieve a list of questions filtered by a query term.

        The query parameter ``q`` must be specified with some text for this function be called.

        Returns:
           If there's no questions when applying the query term, then will result in a dictionary containing a\
           empty list of questions, a empty list of categories, the current category with value of 0 and the total\
           of questions will be a value of 0 too.

           if the query term results in one or more questions, then will result in a dictionary containing a list of\
           questions, a list of categories, the current category and the total of questions regardless the pagination.

        Raises:
            HTTPException(400): If the given query term is empty.

        """
        query_term = request.args.get("q", "", type=str)

        if not query_term:
            abort(400)

        selection = (
            Question.query.filter(
                Question.question.ilike(f"%{query_term}%")
            ).all()
            if query_term
            else []
        )

        if not len(selection):
            return jsonify(
                {"questions": [], "total_questions": 0, "current_category": 0}
            )

        result_questions = [q.format() for q in selection]

        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        return jsonify(
            {
                "questions": result_questions[start:end],
                "total_questions": len(selection),
                "current_category": 0,
            }
        )

    @app.route("/api/categories")
    def get_categories():
        """Get a list of categories.
        ---
        tags:
          - categories
        produces:
          - application/json
        responses:
          200:
            description: A list of categories.
            schema:
              type: array
              items:
                $ref: '#/definitions/Category'
              example: [{"id":1,"type":"Science"},{"id":2,"type":"Art"},{"id":3,"type":"Geography"}]

        """
        return jsonify(query_all_categories())

    def query_all_categories():
        """Query a list of all categories.

         Returns:
             A list of categories.

         """
        selection = Category.query.all()
        result_categories = [c.format() for c in selection]
        return result_categories

    @app.route("/api/questions/<int:question_id>", methods=["DELETE"])
    def remove_question(question_id):
        """Remove a specific question by ID.
        ---
        tags:
          - questions
        parameters:
          - name: question_id
            in: path
            type: integer
            required: true
            description: The ID of the specific question.
        responses:
          500:
            description: If the question can't be removed or something goes wrong within our end.
          404:
            description: If the given ID doesn't exists.
          204:
            description: No content.

        """
        question = Question.query.filter_by(id=question_id).first()

        if question is None:
            abort(404)

        try:
            question.delete()
            return jsonify(None), 204
        except exc.SQLAlchemyError:
            return abort(500)

    @app.route("/api/questions", methods=["POST"])
    def add_question():
        """Add a new question.
        ---
        tags:
          - questions
        parameters:
          - name: body
            in: body
            description: The question JSON attributes.
            schema:
              properties:
                question:
                  type: string
                  description: The question itself.
                  required: true
                  example: Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?
                answer:
                  type: string
                  description: The answer of the question.
                  required: true
                  example: Maya Angelou
                category:
                  type: integer
                  description: The category the question is related of.
                  required: true
                  example: 4
                difficulty:
                  type: integer
                  description: The degree of difficulty, in a range from 1 to 5.
                  required: true
                  example: 2
        consumes:
          - application/json
        produces:
          - application/json
        responses:
          500:
            description: If something goes wrong within our end.
          400:
            description: If one of the required parameters were missing.
          201:
            description: The new created question.
            schema:
              $ref: '#/definitions/Question'

        """
        body = request.get_json()
        if body is None:
            abort(400)

        question = body.get("question", None)
        answer = body.get("answer", None)
        category = body.get("category", None)
        difficulty = body.get("difficulty", None)

        if not all([question, answer, category, difficulty]):
            abort(400)

        try:
            new_question = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty,
            )
            new_question.insert()

            return jsonify(new_question.format()), 201
        except exc.SQLAlchemyError:
            return abort(500)

    @app.route("/api/quizzes", methods=["POST"])
    def play_game():
        """Get next question of the current quiz.
        ---
        tags:
          - quizzes
        parameters:
          - name: body
            in: body
            description: The quiz JSON attributes.
            schema:
              properties:
                previous_questions:
                  type: array
                  description: The list of IDs of the previously answered questions.
                  example: [20, 21, 22]
                quiz_category:
                  description: The category selected for current quiz.
                  $ref: '#/definitions/Category'
        consumes:
          - application/json
        produces:
          - application/json
        definitions:
          Quiz:
            type: object
            properties:
              question:
                $ref: '#/definitions/Question'
              quiz_category:
                $ref: '#/definitions/Category'
        responses:
          200:
            description: The next question of the current quiz.
            schema:
              $ref: '#/definitions/Quiz'

        """
        body = request.get_json()
        if body is None:
            previous_questions = []
            quiz_category = {}
        else:
            previous_questions = body.get("previous_questions", [])
            quiz_category = body.get("quiz_category", {})

        selection = (
            Question.query.all()
            if quiz_category is None or "id" not in quiz_category
            else Question.query.order_by(Question.id)
            .filter_by(category=str(quiz_category["id"]))
            .all()
        )

        question = None
        if len(previous_questions):
            question = next(
                (q for q in selection if q.id not in previous_questions), None
            )
        else:
            question = selection[0]

        if question is None:
            question = next(
                (q for q in selection if q.id == previous_questions[0]),
                selection[0],
            )

        result_question = question.format()
        category = (
            Category.query.filter_by(id=str(result_question["category"]))
            .first()
            .format()
        )

        return jsonify(
            {"question": result_question, "quiz_category": category}
        )

    def handle_error(e):
        """Generic error handler for registered all HTTP errors.

        Args:
            e (~werkzeug.exceptions.HTTPException) : The HTTP exception.

        Returns:
           The jsonified error response.

        """
        error_code = e.code
        error, message = str(e).split(":", 1)

        errors = [
            dict(
                code=error_code,
                error=error,
                message=message.strip(),
                path=request.path,
            )
        ]
        return jsonify(errors=errors), error_code

    for code in default_exceptions:
        app.register_error_handler(code, handle_error)

    return app
