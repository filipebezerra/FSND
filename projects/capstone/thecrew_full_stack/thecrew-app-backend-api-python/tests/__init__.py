import unittest
from app import create_app, db
from app.models import Gender


class BaseAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(FORCE_ENV_FOR_DYNACONF='testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.endpoints = {
            'actors': f'/api/{self.app.config["THECREW_API_VERSION"]}/actors',
            'movies': f'/api/{self.app.config["THECREW_API_VERSION"]}/movies'
        }

    def tearDown(self):
        self.app_context.pop()


class BaseDBTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        super().tearDown()


class BaseDBWithGendersTestCase(BaseDBTestCase):
    def setUp(self):
        super().setUp()
        Gender.insert_genders()
