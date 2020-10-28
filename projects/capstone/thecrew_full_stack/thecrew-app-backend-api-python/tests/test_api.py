from datetime import datetime, timedelta
import json
import requests
import unittest
from tests import BaseDBWithGendersTestCase
from app import db
from app.models import Gender, Actor, Movie
from app.date import now

_cached_auth_headers = {'token': {}, 'token_date': None, 'token_scope': None}


class APITestCase(BaseDBWithGendersTestCase):
    @classmethod
    def setUpClass(cls):
        cls.roles = {
            'casting_assistant': ('view:actors view:movies'),
            'casting_director': (
                'view:actors add:actors edit:actors delete:actors '
                'view:movies edit:movies'),
            'executive_producer': (
                'view:actors add:actors edit:actors delete:actors '
                'view:movies add:movies edit:movies delete:movies')
        }

    def _set_cached_auth_headers(self, **kwargs):
        global _cached_auth_headers
        for k in kwargs:
            _cached_auth_headers[k] = kwargs[k]

    def _is_auth_token_expired(self):
        if not _cached_auth_headers['token']:
            return False
        expires_in = _cached_auth_headers['token']['expires_in']
        token_date = _cached_auth_headers['token_date']
        return token_date + timedelta(seconds=expires_in) < \
            now() + timedelta(seconds=60)

    def _has_different_scope(self, scope):
        return _cached_auth_headers['token_scope'] != scope

    def _set_auth_token(self, token, scope):
        self._set_cached_auth_headers(token=token)
        self._set_cached_auth_headers(token_scope=scope)
        self._set_cached_auth_headers(token_date=now())

    def _get_auth_token(self):
        return f'{_cached_auth_headers["token"]["token_type"]} \
            {_cached_auth_headers["token"]["access_token"]}' \
                if _cached_auth_headers['token'] else None

    def _build_auth_token_payload(self, scope):
        payload = {
            'client_id': self.app.config['AUTH0_CLIENT_ID'],
            'client_secret': self.app.config['AUTH0_CLIENT_SECRET'],
            'audience': self.app.config['AUTH0_API_AUDIENCE'],
            'grant_type': self.app.config['AUTH0_GRANT_TYPE']
        }
        if scope:
            payload['scope'] = scope
        return payload

    def _request_auth_token(self, scope):
        url = f'https://{self.app.config["AUTH0_DOMAIN"]}/oauth/token'
        payload = self._build_auth_token_payload(scope)
        response = requests.post(url, json=payload)
        self.assertEqual(
            response.status_code,
            200,
            msg=f'Could not request auth token: {response.reason}')
        self._set_auth_token(response.json(), scope)

    def get_api_headers(self, scope=None):
        if not _cached_auth_headers['token'] or self._is_auth_token_expired() \
                or self._has_different_scope(scope):
            self._request_auth_token(scope)
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': self._get_auth_token()
        }

    def test_crud_actors(self):
        # add a actor
        response = self.client.post(
            self.endpoints['actors'],
            headers=self.get_api_headers(),
            data=json.dumps(
                {
                    'age': 23,
                    'gender': 'Female',
                    'fullName': 'Sanjana Sanghi'
                }))
        self.assertEqual(response.status_code, 201)
        url_actor = response.headers.get('Location')
        self.assertIsNotNone(url_actor)

        movie = Movie(
            title='Dil Bechara',
            release_date=datetime(2020, 7, 24),
            actors=[Actor.query.filter_by(full_name='Sanjana Sanghi').first()])
        db.session.add(movie)
        db.session.commit()

        # get the new actor
        response = self.client.get(url_actor, headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertTrue(json_response['uuid'])
        self.assertEqual(json_response['age'], 23)
        self.assertEqual(json_response['fullName'], 'Sanjana Sanghi')
        self.assertEqual(json_response['gender'], 'Female')
        self.assertEqual(json_response['moviesCount'], 1)
        json_actor = json_response

        # get actors
        response = self.client.get(
            self.endpoints['actors'], headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertIsNotNone(json_response['objects'])
        self.assertEqual(json_response.get('totalCount', 0), 1)
        self.assertEqual(json_response.get('totalPages', 0), 1)
        self.assertEqual(json_response.get('page', 0), 1)
        self.assertEqual(json_response['objects'][0], json_actor)

        # update actor
        response = self.client.patch(
            url_actor,
            headers=self.get_api_headers(),
            data=json.dumps({'age': 24}))
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertEqual(json_response['uuid'], json_actor['uuid'])
        self.assertEqual(json_response['age'], 24)
        self.assertEqual(json_response['fullName'], 'Sanjana Sanghi')
        self.assertEqual(json_response['gender'], 'Female')
        self.assertEqual(json_response['moviesCount'], 1)

        # delete actor
        response = self.client.delete(
            url_actor, headers=self.get_api_headers())
        self.assertEqual(response.status_code, 204)

    def test_methods_not_allowed_for_actors(self):
        response = self.client.post(
            self.endpoints['actors'],
            headers=self.get_api_headers(),
            data=json.dumps(
                {
                    'age': 23,
                    'gender': 'Female',
                    'fullName': 'Sanjana Sanghi'
                }))
        url_actor = response.headers.get('Location')

        # put not allowed
        response = self.client.put(
            self.endpoints['actors'],
            headers=self.get_api_headers(),
            data=json.dumps(
                {
                    'age': 23,
                    'gender': 'Female',
                    'fullName': 'Sanjana Sanghi'
                }))
        self.assertEqual(405, response.status_code)

        response = self.client.put(
            url_actor,
            headers=self.get_api_headers(),
            data=json.dumps(
                {
                    'age': 23,
                    'gender': 'Female',
                    'fullName': 'Sanjana Sanghi'
                }))
        self.assertEqual(405, response.status_code)

        # post/<uuid> not allowed
        response = self.client.post(
            url_actor,
            headers=self.get_api_headers(),
            data=json.dumps(
                {
                    'age': 23,
                    'gender': 'Female',
                    'fullName': 'Sanjana Sanghi'
                }))
        self.assertEqual(405, response.status_code)

        # patch all not allowed
        response = self.client.patch(
            self.endpoints['actors'],
            headers=self.get_api_headers(),
            data=json.dumps({'age': 24}))
        self.assertEqual(405, response.status_code)

        # delete all not allowed
        response = self.client.patch(
            self.endpoints['actors'], headers=self.get_api_headers())
        self.assertEqual(405, response.status_code)

    def add_actor(self):
        actor = Actor(
            age=23,
            full_name='Sanjana Sanghi',
            gender=Gender.query.filter_by(name='Female').first())
        db.session.add(actor)
        db.session.commit()
        return actor

    def test_cannot_get_actor_with_int_id(self):
        self.add_actor()

        response = self.client.get(
            self.endpoints['actors'] + '/1', headers=self.get_api_headers())
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.json)
        self.assertIsNotNone(response.json['message'])

    def test_cannot_patch_actor_with_int_id(self):
        self.add_actor()

        response = self.client.patch(
            self.endpoints['actors'] + '/1',
            headers=self.get_api_headers(),
            data=json.dumps({'age': 24}))
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.json)
        self.assertIsNotNone(response.json['message'])

    def test_cannot_delete_actor_with_int_id(self):
        self.add_actor()

        response = self.client.delete(
            self.endpoints['actors'] + '/1', headers=self.get_api_headers())
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.json)
        self.assertIsNotNone(response.json['message'])

    def test_crud_movies(self):
        # add a movie
        actors = [
            Actor(
                age=23,
                full_name='Sanjana Sanghi',
                gender=Gender.query.filter_by(name='Female').first()),
            Actor(
                age=49,
                full_name='Saswata Chatterjee',
                gender=Gender.query.filter_by(name='Male').first()),
            Actor(
                age=49,
                full_name='Saif Ali Khan',
                gender=Gender.query.filter_by(name='Male').first())
        ]
        db.session.add_all(actors)
        db.session.commit()

        response = self.client.post(
            self.endpoints['movies'],
            headers=self.get_api_headers(),
            data=json.dumps(
                {
                    'title': 'Dil Bechara',
                    'releaseDate': '2020-07-24',
                    'actors': [a.to_json() for a in actors]
                }))
        self.assertEqual(response.status_code, 201)
        url_movie = response.headers.get('Location')
        self.assertIsNotNone(url_movie)

        # get the new movie
        response = self.client.get(url_movie, headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertTrue(json_response['uuid'])
        self.assertEqual(json_response['title'], 'Dil Bechara')
        self.assertEqual(json_response['releaseDate'], '2020-07-24')
        self.assertEqual(len(json_response['actors']), 3)
        self.assertListEqual(
            json_response['actors'], [a.to_json() for a in actors])
        json_movie = json_response

        # get movies
        response = self.client.get(
            self.endpoints['movies'], headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertIsNotNone(json_response['objects'])
        self.assertEqual(json_response.get('totalCount', 0), 1)
        self.assertEqual(json_response.get('totalPages', 0), 1)
        self.assertEqual(json_response.get('page', 0), 1)
        self.assertEqual(json_response['objects'][0], json_movie)

        # update movie
        response = self.client.patch(
            url_movie,
            headers=self.get_api_headers(),
            data=json.dumps({'releaseDate': '2020-07-31'}))
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertEqual(json_response['uuid'], json_movie['uuid'])
        self.assertEqual(json_response['title'], 'Dil Bechara')
        self.assertEqual(json_response['releaseDate'], '2020-07-31')
        self.assertEqual(len(json_response['actors']), 3)
        self.assertListEqual(
            json_response['actors'], [a.to_json() for a in actors])

        # delete movie
        response = self.client.delete(
            url_movie, headers=self.get_api_headers())
        self.assertEqual(response.status_code, 204)

    def test_methods_not_allowed_for_movies(self):
        actors = [
            Actor(
                age=23,
                full_name='Sanjana Sanghi',
                gender=Gender.query.filter_by(name='Female').first()),
            Actor(
                age=49,
                full_name='Saswata Chatterjee',
                gender=Gender.query.filter_by(name='Male').first()),
            Actor(
                age=49,
                full_name='Saif Ali Khan',
                gender=Gender.query.filter_by(name='Male').first())
        ]
        db.session.add_all(actors)
        db.session.commit()

        response = self.client.post(
            self.endpoints['movies'],
            headers=self.get_api_headers(),
            data=json.dumps(
                {
                    'title': 'Dil Bechara',
                    'releaseDate': '2020-07-24',
                    'actors': [a.to_json() for a in actors]
                }))
        url_movie = response.headers.get('Location')

        # put not allowed
        response = self.client.put(
            self.endpoints['movies'],
            headers=self.get_api_headers(),
            data=json.dumps(
                {
                    'title': 'Dil Bechara',
                    'releaseDate': '2020-07-24',
                    'actors': [a.to_json() for a in actors]
                }))
        self.assertEqual(405, response.status_code)

        response = self.client.put(
            url_movie,
            headers=self.get_api_headers(),
            data=json.dumps(
                {
                    'title': 'Dil Bechara',
                    'releaseDate': '2020-07-24',
                    'actors': [a.to_json() for a in actors]
                }))
        self.assertEqual(405, response.status_code)

        # post/<uuid> not allowed
        response = self.client.post(
            url_movie,
            headers=self.get_api_headers(),
            data=json.dumps(
                {
                    'title': 'Dil Bechara',
                    'releaseDate': '2020-07-24',
                    'actors': [a.to_json() for a in actors]
                }))
        self.assertEqual(405, response.status_code)

        # patch all not allowed
        response = self.client.patch(
            self.endpoints['movies'],
            headers=self.get_api_headers(),
            data=json.dumps({'releaseDate': '2020-07-31'}))
        self.assertEqual(405, response.status_code)

        # delete all not allowed
        response = self.client.delete(
            self.endpoints['movies'], headers=self.get_api_headers())
        self.assertEqual(405, response.status_code)

    def add_movie(self):
        actor = Actor(
            age=23,
            full_name='Sanjana Sanghi',
            gender=Gender.query.filter_by(name='Female').first())
        db.session.add(actor)
        db.session.commit()

        movie = Movie(
            title='Dil Bechara',
            release_date=datetime(2020, 7, 24),
            actors=[actor])
        db.session.add(movie)
        db.session.commit()
        return movie

    def test_cannot_get_movie_with_int_id(self):
        self.add_movie()

        response = self.client.get(
            self.endpoints['movies'] + '/1', headers=self.get_api_headers())
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.json)
        self.assertIsNotNone(response.json['message'])

    def test_cannot_patch_movie_with_int_id(self):
        self.add_movie()

        response = self.client.patch(
            self.endpoints['movies'] + '/1',
            headers=self.get_api_headers(),
            data=json.dumps({'releaseDate': '2020-07-31'}))
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.json)
        self.assertIsNotNone(response.json['message'])

    def test_cannot_delete_movie_with_int_id(self):
        self.add_movie()

        response = self.client.delete(
            self.endpoints['movies'] + '/1', headers=self.get_api_headers())
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.json)
        self.assertIsNotNone(response.json['message'])

    def test_cannot_post_movie_without_body(self):
        response = self.client.post(
            self.endpoints['movies'], headers=self.get_api_headers(), json='')
        self.assertEqual(response.status_code, 400)
        json_response = response.json
        self.assertEqual(len(json_response.get('errors', 0)), 3)
        self.assertListEqual(
            [e.get('code') for e in json_response.get('errors')],
            ['missing_field', 'missing_field', 'missing_field'])
        self.assertListEqual(
            sorted([e.get('field') for e in json_response.get('errors')]),
            ['actors', 'releaseDate', 'title'])

    def test_cannot_patch_movie_without_body(self):
        movie = self.add_movie()

        response = self.client.patch(
            f'{self.endpoints["movies"]}/{movie.uuid}',
            headers=self.get_api_headers(),
            json='')
        self.assertEqual(response.status_code, 400)
        json_response = response.json
        self.assertEqual(len(json_response.get('errors', 0)), 1)
        self.assertEqual(
            json_response.get('errors')[0]['code'], 'missing_field')
        self.assertIn('actors', json_response.get('errors')[0]['description'])
        self.assertIn(
            'releaseDate',
            json_response.get('errors')[0]['description'])
        self.assertIn('title', json_response.get('errors')[0]['description'])

    def test_cannot_post_actor_without_body(self):
        response = self.client.post(
            self.endpoints['actors'], headers=self.get_api_headers(), json='')
        self.assertEqual(response.status_code, 400)
        json_response = response.json
        self.assertEqual(len(json_response.get('errors', 0)), 3)
        self.assertListEqual(
            [e.get('code') for e in json_response.get('errors')],
            ['missing_field', 'missing_field', 'missing_field'])
        self.assertListEqual(
            sorted([e.get('field') for e in json_response.get('errors')]),
            ['age', 'fullName', 'gender'])

    def test_cannot_patch_actor_without_body(self):
        actor = self.add_actor()

        response = self.client.patch(
            f'{self.endpoints["actors"]}/{actor.uuid}',
            headers=self.get_api_headers(),
            json='')
        self.assertEqual(response.status_code, 400)
        json_response = response.json
        self.assertEqual(len(json_response.get('errors', 0)), 1)
        self.assertEqual(
            json_response.get('errors')[0]['code'], 'missing_field')
        self.assertIn('age', json_response.get('errors')[0]['description'])
        self.assertIn(
            'fullName',
            json_response.get('errors')[0]['description'])
        self.assertIn('gender', json_response.get('errors')[0]['description'])

    def test_casting_assistant_can_view_actors(self):
        actor = self.add_actor()
        response = self.client.get(
            self.endpoints['actors'],
            headers=self.get_api_headers(self.roles['casting_assistant']))
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertIsNotNone(json_response['objects'])
        self.assertEqual(json_response.get('totalCount', 0), 1)
        self.assertEqual(json_response.get('totalPages', 0), 1)
        self.assertEqual(json_response.get('page', 0), 1)
        self.assertEqual(json_response['objects'][0]['uuid'], str(actor.uuid))
        self.assertEqual(
            json_response['objects'][0]['fullName'], 'Sanjana Sanghi')
        self.assertEqual(json_response['objects'][0]['age'], 23)
        self.assertEqual(json_response['objects'][0]['gender'], 'Female')

    def test_casting_assistant_can_view_movies(self):
        movie = self.add_movie()
        response = self.client.get(
            self.endpoints['movies'],
            headers=self.get_api_headers(self.roles['casting_assistant']))
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertIsNotNone(json_response['objects'])
        self.assertEqual(json_response.get('totalCount', 0), 1)
        self.assertEqual(json_response.get('totalPages', 0), 1)
        self.assertEqual(json_response.get('page', 0), 1)
        self.assertEqual(json_response['objects'][0]['uuid'], str(movie.uuid))
        self.assertEqual(json_response['objects'][0]['title'], 'Dil Bechara')
        self.assertEqual(
            json_response['objects'][0]['releaseDate'], '2020-07-24')
        self.assertEqual(len(json_response['objects'][0]['actors']), 1)
        self.assertListEqual(
            json_response['objects'][0]['actors'],
            [a.to_json() for a in movie.actors])

    def test_casting_assistant_cannot_add_actors(self):
        response = self.client.post(
            self.endpoints['actors'],
            headers=self.get_api_headers(self.roles['casting_assistant']),
            data=json.dumps(
                {
                    'age': 23,
                    'gender': 'Female',
                    'fullName': 'Sanjana Sanghi'
                }))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json['errors'][0]['code'], 'unauthorized')
        self.assertEqual(
            response.json['errors'][0]['description'], 'Permission not found')

    def test_casting_assistant_cannot_add_movies(self):
        actors = [
            Actor(
                age=23,
                full_name='Sanjana Sanghi',
                gender=Gender.query.filter_by(name='Female').first()),
            Actor(
                age=49,
                full_name='Saswata Chatterjee',
                gender=Gender.query.filter_by(name='Male').first()),
            Actor(
                age=49,
                full_name='Saif Ali Khan',
                gender=Gender.query.filter_by(name='Male').first())
        ]
        db.session.add_all(actors)
        db.session.commit()

        response = self.client.post(
            self.endpoints['movies'],
            headers=self.get_api_headers(self.roles['casting_assistant']),
            data=json.dumps(
                {
                    'title': 'Dil Bechara',
                    'releaseDate': '2020-07-24',
                    'actors': [a.to_json() for a in actors]
                }))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json['errors'][0]['code'], 'unauthorized')
        self.assertEqual(
            response.json['errors'][0]['description'], 'Permission not found')

    def test_casting_assistant_cannot_update_actors(self):
        actor = self.add_actor()

        response = self.client.patch(
            f'{self.endpoints["actors"]}/{actor.uuid}',
            headers=self.get_api_headers(self.roles['casting_assistant']),
            data=json.dumps({'age': 24}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json['errors'][0]['code'], 'unauthorized')
        self.assertEqual(
            response.json['errors'][0]['description'], 'Permission not found')

    def test_casting_assistant_cannot_update_movies(self):
        movie = self.add_movie()

        response = self.client.patch(
            f'{self.endpoints["movies"]}/{movie.uuid}',
            headers=self.get_api_headers(self.roles['casting_assistant']),
            data=json.dumps({'releaseDate': '2020-07-31'}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json['errors'][0]['code'], 'unauthorized')
        self.assertEqual(
            response.json['errors'][0]['description'], 'Permission not found')

    def test_casting_assistant_cannot_delete_actors(self):
        actor = self.add_actor()

        response = self.client.delete(
            f'{self.endpoints["actors"]}/{actor.uuid}',
            headers=self.get_api_headers(self.roles['casting_assistant']))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json['errors'][0]['code'], 'unauthorized')
        self.assertEqual(
            response.json['errors'][0]['description'], 'Permission not found')

    def test_casting_assistant_cannot_delete_movies(self):
        movie = self.add_movie()

        response = self.client.delete(
            f'{self.endpoints["movies"]}/{movie.uuid}',
            headers=self.get_api_headers(self.roles['casting_assistant']))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json['errors'][0]['code'], 'unauthorized')
        self.assertEqual(
            response.json['errors'][0]['description'], 'Permission not found')

    def test_casting_director_can_view_actors(self):
        actor = self.add_actor()
        response = self.client.get(
            self.endpoints['actors'],
            headers=self.get_api_headers(self.roles['casting_director']))
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertIsNotNone(json_response['objects'])
        self.assertEqual(json_response.get('totalCount', 0), 1)
        self.assertEqual(json_response.get('totalPages', 0), 1)
        self.assertEqual(json_response.get('page', 0), 1)
        self.assertEqual(json_response['objects'][0]['uuid'], str(actor.uuid))
        self.assertEqual(
            json_response['objects'][0]['fullName'], 'Sanjana Sanghi')
        self.assertEqual(json_response['objects'][0]['age'], 23)
        self.assertEqual(json_response['objects'][0]['gender'], 'Female')

    def test_casting_director_can_view_movies(self):
        movie = self.add_movie()
        response = self.client.get(
            self.endpoints['movies'],
            headers=self.get_api_headers(self.roles['casting_director']))
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertIsNotNone(json_response['objects'])
        self.assertEqual(json_response.get('totalCount', 0), 1)
        self.assertEqual(json_response.get('totalPages', 0), 1)
        self.assertEqual(json_response.get('page', 0), 1)
        self.assertEqual(json_response['objects'][0]['uuid'], str(movie.uuid))
        self.assertEqual(json_response['objects'][0]['title'], 'Dil Bechara')
        self.assertEqual(
            json_response['objects'][0]['releaseDate'], '2020-07-24')
        self.assertEqual(len(json_response['objects'][0]['actors']), 1)
        self.assertListEqual(
            json_response['objects'][0]['actors'],
            [a.to_json() for a in movie.actors])

    def test_casting_director_can_add_actors(self):
        response = self.client.post(
            self.endpoints['actors'],
            headers=self.get_api_headers(self.roles['casting_director']),
            data=json.dumps(
                {
                    'age': 23,
                    'gender': 'Female',
                    'fullName': 'Sanjana Sanghi'
                }))
        self.assertEqual(response.status_code, 201)
        json_response = response.json
        self.assertIsNotNone(json_response['uuid'])
        self.assertEqual(json_response['age'], 23)
        self.assertEqual(json_response['fullName'], 'Sanjana Sanghi')
        self.assertEqual(json_response['gender'], 'Female')
        self.assertEqual(json_response['moviesCount'], 0)

    def test_casting_director_cannot_add_movies(self):
        actors = [
            Actor(
                age=23,
                full_name='Sanjana Sanghi',
                gender=Gender.query.filter_by(name='Female').first()),
            Actor(
                age=49,
                full_name='Saswata Chatterjee',
                gender=Gender.query.filter_by(name='Male').first()),
            Actor(
                age=49,
                full_name='Saif Ali Khan',
                gender=Gender.query.filter_by(name='Male').first())
        ]
        db.session.add_all(actors)
        db.session.commit()

        response = self.client.post(
            self.endpoints['movies'],
            headers=self.get_api_headers(self.roles['casting_director']),
            data=json.dumps(
                {
                    'title': 'Dil Bechara',
                    'releaseDate': '2020-07-24',
                    'actors': [a.to_json() for a in actors]
                }))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json['errors'][0]['code'], 'unauthorized')
        self.assertEqual(
            response.json['errors'][0]['description'], 'Permission not found')

    def test_casting_director_can_update_actors(self):
        actor = self.add_actor()

        response = self.client.patch(
            f'{self.endpoints["actors"]}/{actor.uuid}',
            headers=self.get_api_headers(self.roles['casting_director']),
            data=json.dumps({'age': 24}))
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertEqual(json_response['uuid'], str(actor.uuid))
        self.assertEqual(json_response['age'], 24)
        self.assertEqual(json_response['fullName'], 'Sanjana Sanghi')
        self.assertEqual(json_response['gender'], 'Female')
        self.assertEqual(json_response['moviesCount'], 0)

    def test_casting_director_can_update_movies(self):
        movie = self.add_movie()

        response = self.client.patch(
            f'{self.endpoints["movies"]}/{movie.uuid}',
            headers=self.get_api_headers(self.roles['casting_director']),
            data=json.dumps({'releaseDate': '2020-07-31'}))
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertEqual(json_response['uuid'], str(movie.uuid))
        self.assertEqual(json_response['title'], 'Dil Bechara')
        self.assertEqual(json_response['releaseDate'], '2020-07-31')
        self.assertEqual(len(json_response['actors']), 1)
        self.assertListEqual(
            json_response['actors'], [a.to_json() for a in movie.actors])

    def test_casting_director_can_delete_actors(self):
        actor = self.add_actor()

        response = self.client.delete(
            f'{self.endpoints["actors"]}/{actor.uuid}',
            headers=self.get_api_headers(self.roles['casting_director']))
        self.assertEqual(response.status_code, 204)

    def test_casting_director_cannot_delete_movies(self):
        movie = self.add_movie()

        response = self.client.delete(
            f'{self.endpoints["movies"]}/{movie.uuid}',
            headers=self.get_api_headers(self.roles['casting_director']))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json['errors'][0]['code'], 'unauthorized')
        self.assertEqual(
            response.json['errors'][0]['description'], 'Permission not found')

    def test_executive_producer_can_view_actors(self):
        actor = self.add_actor()
        response = self.client.get(
            self.endpoints['actors'],
            headers=self.get_api_headers(self.roles['executive_producer']))
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertIsNotNone(json_response['objects'])
        self.assertEqual(json_response.get('totalCount', 0), 1)
        self.assertEqual(json_response.get('totalPages', 0), 1)
        self.assertEqual(json_response.get('page', 0), 1)
        self.assertEqual(json_response['objects'][0]['uuid'], str(actor.uuid))
        self.assertEqual(
            json_response['objects'][0]['fullName'], 'Sanjana Sanghi')
        self.assertEqual(json_response['objects'][0]['age'], 23)
        self.assertEqual(json_response['objects'][0]['gender'], 'Female')

    def test_executive_producer_can_view_movies(self):
        movie = self.add_movie()
        response = self.client.get(
            self.endpoints['movies'],
            headers=self.get_api_headers(self.roles['executive_producer']))
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertIsNotNone(json_response['objects'])
        self.assertEqual(json_response.get('totalCount', 0), 1)
        self.assertEqual(json_response.get('totalPages', 0), 1)
        self.assertEqual(json_response.get('page', 0), 1)
        self.assertEqual(json_response['objects'][0]['uuid'], str(movie.uuid))
        self.assertEqual(json_response['objects'][0]['title'], 'Dil Bechara')
        self.assertEqual(
            json_response['objects'][0]['releaseDate'], '2020-07-24')
        self.assertEqual(len(json_response['objects'][0]['actors']), 1)
        self.assertListEqual(
            json_response['objects'][0]['actors'],
            [a.to_json() for a in movie.actors])

    def test_executive_producer_can_add_actors(self):
        response = self.client.post(
            self.endpoints['actors'],
            headers=self.get_api_headers(self.roles['executive_producer']),
            data=json.dumps(
                {
                    'age': 23,
                    'gender': 'Female',
                    'fullName': 'Sanjana Sanghi'
                }))
        self.assertEqual(response.status_code, 201)
        json_response = response.json
        self.assertIsNotNone(json_response['uuid'])
        self.assertEqual(json_response['age'], 23)
        self.assertEqual(json_response['fullName'], 'Sanjana Sanghi')
        self.assertEqual(json_response['gender'], 'Female')
        self.assertEqual(json_response['moviesCount'], 0)

    def test_executive_producer_can_add_movies(self):
        actors = [
            Actor(
                age=23,
                full_name='Sanjana Sanghi',
                gender=Gender.query.filter_by(name='Female').first()),
            Actor(
                age=49,
                full_name='Saswata Chatterjee',
                gender=Gender.query.filter_by(name='Male').first()),
            Actor(
                age=49,
                full_name='Saif Ali Khan',
                gender=Gender.query.filter_by(name='Male').first())
        ]
        db.session.add_all(actors)
        db.session.commit()

        response = self.client.post(
            self.endpoints['movies'],
            headers=self.get_api_headers(self.roles['executive_producer']),
            data=json.dumps(
                {
                    'title': 'Dil Bechara',
                    'releaseDate': '2020-07-24',
                    'actors': [a.to_json() for a in actors]
                }))
        self.assertEqual(response.status_code, 201)
        json_response = response.json
        self.assertTrue(json_response['uuid'])
        self.assertEqual(json_response['title'], 'Dil Bechara')
        self.assertEqual(json_response['releaseDate'], '2020-07-24')
        self.assertEqual(len(json_response['actors']), 3)
        self.assertListEqual(
            json_response['actors'], [a.to_json() for a in actors])

    def test_executive_producer_can_update_actors(self):
        actor = self.add_actor()

        response = self.client.patch(
            f'{self.endpoints["actors"]}/{actor.uuid}',
            headers=self.get_api_headers(self.roles['executive_producer']),
            data=json.dumps({'age': 24}))
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertEqual(json_response['uuid'], str(actor.uuid))
        self.assertEqual(json_response['age'], 24)
        self.assertEqual(json_response['fullName'], 'Sanjana Sanghi')
        self.assertEqual(json_response['gender'], 'Female')
        self.assertEqual(json_response['moviesCount'], 0)

    def test_executive_producer_can_update_movies(self):
        movie = self.add_movie()

        response = self.client.patch(
            f'{self.endpoints["movies"]}/{movie.uuid}',
            headers=self.get_api_headers(self.roles['executive_producer']),
            data=json.dumps({'releaseDate': '2020-07-31'}))
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertEqual(json_response['uuid'], str(movie.uuid))
        self.assertEqual(json_response['title'], 'Dil Bechara')
        self.assertEqual(json_response['releaseDate'], '2020-07-31')
        self.assertEqual(len(json_response['actors']), 1)
        self.assertListEqual(
            json_response['actors'], [a.to_json() for a in movie.actors])

    def test_executive_producer_can_delete_actors(self):
        actor = self.add_actor()

        response = self.client.delete(
            f'{self.endpoints["actors"]}/{actor.uuid}',
            headers=self.get_api_headers(self.roles['executive_producer']))
        self.assertEqual(response.status_code, 204)

    def test_executive_producer_cannot_delete_movies(self):
        movie = self.add_movie()

        response = self.client.delete(
            f'{self.endpoints["movies"]}/{movie.uuid}',
            headers=self.get_api_headers(self.roles['executive_producer']))
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
