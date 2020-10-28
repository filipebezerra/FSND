import unittest
from uuid import uuid4
from flask import current_app
from tests import BaseDBWithGendersTestCase
from app import db


class PrerequisitesTestCase(BaseDBWithGendersTestCase):
    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_db_exists(self):
        self.assertIsNotNone(db)

    def test_db_is_readable(self):
        result = db.session.execute('SELECT * FROM movies')
        self.assertEqual(len(result.fetchall()), 0)

    def test_db_is_writable(self):
        db.session.execute(
            (
                'INSERT INTO movies (uuid, title, release_date) '
                'VALUES (:uuid, :title, :release_date)'), {
                    'uuid': str(uuid4()),
                    'title': 'Dil Bechara',
                    'release_date': '2020-07-24'
                })
        result = db.session.execute(
            'SELECT * FROM movies WHERE title = :title',
            {'title': 'Dil Bechara'})
        movie = result.first()
        self.assertEqual(movie['title'], 'Dil Bechara')
        self.assertEqual(movie['release_date'], '2020-07-24')


if __name__ == '__main__':
    unittest.main()
