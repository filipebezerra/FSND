import os
import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, QUESTIONS_PER_PAGE
from models import setup_db, Question, Category

DATABASE_NAME = os.getenv("TEST_DB_NAME")
DATABASE_USER = os.getenv("TEST_DB_USER")
DATABASE_HOST = os.getenv("TEST_DB_HOST")
DATABASE_PASSWORD = os.getenv("TEST_DB_PASSWORD")


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_path = f'postgresql://{DATABASE_USER}:\
            {DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'
        # binds the app to the current context
        self.ctx = self.app.app_context()
        self.ctx.push()
        setup_db(self.app, self.database_path)

        self.db = SQLAlchemy()
        self.db.init_app(self.app)
        # create all tables
        self.db.create_all()

        self.new_question = {
            "question": "In which year the Great Depression started "
                        "in United States",
            "answer": "1929",
            "category": 4,
            "difficulty": 2,
        }
        self.search_question = "american"
        self.game = {"quiz_category": None, "previous_questions": []}

    def tearDown(self):
        """Executed after reach test"""
        self.db.session.remove()
        self.db.drop_all()
        self.ctx.pop()

    def test_can_get_categories(self):
        """Test API can get all categories"""
        total_of_categories = Category.query.count()

        response = self.client.get("/api/categories")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), total_of_categories)
        self.assertTrue(data[0]["id"])
        self.assertTrue(data[0]["type"])

    def test_405_when_post_categories(self):
        """
        Test API responses with 405 Method Not Allowed when
        requesting categories using POST
        """
        response = self.client.post("/api/categories")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertTrue(len(data["errors"]))
        self.assertEqual(data["errors"][0]["code"], 405)
        self.assertEqual(data["errors"][0]["error"], "405 Method Not Allowed")

    def test_get_questions(self):
        """
        Test API can get questions related to first category
        ordered by category type
        """
        total_of_categories = Category.query.count()
        first_category = Category.query.order_by(Category.type.asc()).first()
        questions = Question.query.filter_by(
            category=str(first_category.id)
        ).all()

        response = self.client.get("/api/questions")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(data["questions"]), len(questions[0:QUESTIONS_PER_PAGE])
        )
        self.assertEqual(data["total_questions"], len(questions))
        self.assertEqual(data["current_category"], first_category.id)
        self.assertEqual(len(data["categories"]), total_of_categories)

    def test_get_paginated_books(self):
        """Test API can get all existing questions with page"""
        total_of_categories = Category.query.count()
        first_category = Category.query.order_by(Category.type.asc()).first()
        questions = Question.query.filter_by(
            category=str(first_category.id)
        ).all()

        response = self.client.get("/api/questions?page=1")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(data["questions"]), len(questions[0:QUESTIONS_PER_PAGE])
        )
        self.assertEqual(data["total_questions"], len(questions))
        self.assertEqual(data["current_category"], first_category.id)
        self.assertEqual(len(data["categories"]), total_of_categories)

    def test_404_when_get_paginated_questions(self):
        """
        Test API responses with 404 Not Found when requesting questions
        with unreacheable page
        """
        response = self.client.get("/api/questions?page=999999")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(len(data["errors"]))
        self.assertEqual(data["errors"][0]["code"], 404)
        self.assertEqual(data["errors"][0]["error"], "404 Not Found")

    def test_get_questions_by_category(self):
        """
        Test API can get questions related to specific category
        """
        total_of_categories = Category.query.count()
        questions = Question.query.filter_by(category="1").all()

        response = self.client.get("/api/categories/1/questions")
        data = json.loads(response.data)
        self.assertEqual(
            len(data["questions"]), len(questions[0:QUESTIONS_PER_PAGE])
        )
        self.assertEqual(data["total_questions"], len(questions))
        self.assertEqual(data["current_category"], 1)
        self.assertEqual(len(data["categories"]), total_of_categories)

    def test_404_when_get_questions_by_category(self):
        """
        Test API responses with 404 Not Found when requesting questions
        with unexistent category
        """
        response = self.client.get("/api/categories/9999999/questions")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["errors"][0]["code"], 404)
        self.assertEqual(data["errors"][0]["error"], "404 Not Found")

    def test_delete_question(self):
        """Test API can delete a question"""
        question = Question.query.order_by(Question.id).first()
        id = question.id

        response = self.client.delete(f"/api/questions/{id}")
        self.assertEqual(response.status_code, 204)

        deleted = Question.query.filter_by(id=id).first()
        self.assertIsNone(deleted)

    def test_404_when_delete_question(self):
        response = self.client.delete(f"/api/questions/9999999")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["errors"][0]["code"], 404)
        self.assertEqual(data["errors"][0]["error"], "404 Not Found")

    def test_create_question(self):
        """Test API can create a new question"""
        response = self.client.post("/api/questions", json=self.new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone([data["id"]])
        self.assertEqual(data["question"], self.new_question["question"])
        self.assertEqual(data["answer"], self.new_question["answer"])
        self.assertEqual(data["category"], self.new_question["category"])
        self.assertEqual(data["difficulty"], self.new_question["difficulty"])

        created = Question.query.filter_by(id=data["id"]).first()
        self.assertIsNotNone(created)
        self.assertEqual(data["question"], created.question)
        self.assertEqual(data["answer"], created.answer)
        self.assertEqual(data["category"], created.category)
        self.assertEqual(data["difficulty"], created.difficulty)

    def test_400_when_create_question(self):
        """
        Test API responses with Bad request when trying to create
        a question without any of required attributes
        """
        new_question = {
            "question": "Which number",
            "answer": "My answer",
            "category": "1",
        }
        response = self.client.post("/api/questions", json=new_question)
        self.assertEqual(response.status_code, 400)

        not_created = Question.query.filter_by(
            question=new_question["question"],
            answer=new_question["answer"],
            category=new_question["category"],
        ).first()
        self.assertIsNone(not_created)

    def test_search_question(self):
        """Test API can search for questions by a term"""
        questions = Question.query.filter(
            Question.question.ilike(f"%{self.search_question}%")
        ).all()
        results = [q.format() for q in questions]

        response = self.client.get(f"/api/questions?q={self.search_question}")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["questions"]), len(results))
        self.assertEqual(data["current_category"], 0)
        self.assertEqual(data["total_questions"], len(results))

        for q in data["questions"]:
            self.assertIn(
                self.search_question.casefold(), q["question"].casefold()
            )

        self.assertCountEqual(data["questions"], results)
        self.assertListEqual(data["questions"], results)

    def test_search_questions_with_no_results(self):
        """
        Test API responses no questions when an unknown term is used to search
        """
        response = self.client.get("/api/questions?q=lieutenant")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(len(data["questions"]))
        self.assertFalse(data["current_category"])
        self.assertFalse(data["total_questions"])

    def test_400_when_search_questions_with_empty_term(self):
        """
        Test API responses with 400 Bad Request when no query term
        is provided in the request
        """
        response = self.client.get("/api/questions?q=")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"][0]["code"], 400)
        self.assertEqual(data["errors"][0]["error"], "400 Bad Request")

    def test_play_game_with_all_categories(self):
        """
        Test API can play the quiz with any category
        """
        response = self.client.post("/api/quizzes", json=self.game)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["question"])
        self.assertTrue(data["quiz_category"])

    def test_play_game_with_specific_category(self):
        """
        Test API can play the quiz with a specific category
        of questions
        """
        category = 1
        self.game["quiz_category"] = {"id": category}
        response = self.client.post("/api/quizzes", json=self.game)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["question"])
        self.assertEqual(data["question"]["category"], category)
        self.assertTrue(data["question"])
        self.assertEqual(data["quiz_category"]["id"], category)

        self.game["quiz_category"]["id"] = category = 3
        response = self.client.post("/api/quizzes", json=self.game)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["question"])
        self.assertEqual(data["question"]["category"], category)
        self.assertTrue(data["question"])
        self.assertEqual(data["quiz_category"]["id"], category)

    def test_play_game_with_previous_questions(self):
        """
        Test API can play the quiz after the last question
        being answered
        """
        category = 4
        self.game["quiz_category"] = {"id": category}

        for _ in range(5):
            response = self.client.post("/api/quizzes", json=self.game)
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data["question"])
            self.assertTrue(data["question"]["id"])
            self.assertTrue(data["quiz_category"])
            self.assertTrue(data["quiz_category"]["id"])
            self.assertEqual(data["quiz_category"]["id"], category)

            if len(self.game["previous_questions"]):
                self.assertNotIn(
                    data["question"]["id"], self.game["previous_questions"]
                )

            self.game["previous_questions"].append(data["question"]["id"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
