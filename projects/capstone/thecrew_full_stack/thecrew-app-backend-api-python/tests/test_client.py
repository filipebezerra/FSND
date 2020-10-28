import unittest
from tests import BaseAPITestCase


class ClientTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.client = self.app.test_client(use_cookies=True)

    def test_login(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 302)
        self.assertIn('https://the-crew-fsnd.us.auth0.com/authorize',
                      response.headers.get('Location'))
        self.assertEqual(
            len(response.headers.get('Location').split('?')[1].split('&')), 4)

    def test_signup(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 302)
        self.assertIn('https://the-crew-fsnd.us.auth0.com/authorize',
                      response.headers.get('Location'))
        self.assertEqual(
            len(response.headers.get('Location').split('?')[1].split('&')), 4)

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Welcome to TheCrew' in response.get_data(
            as_text=True))

    def test_welcome(self):
        response = self.client.get('/welcome')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Welcome to TheCrew' in response.get_data(
            as_text=True))


if __name__ == '__main__':
    unittest.main()
