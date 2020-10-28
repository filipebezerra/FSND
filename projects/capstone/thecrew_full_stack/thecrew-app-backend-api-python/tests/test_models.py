import unittest
import uuid
from datetime import datetime
from app import db
from tests import BaseDBTestCase
from app.models import Gender, Actor, Movie
from app.date import date_to_str, now
from app.exceptions import ValidationsError


class GenderCrudTestCase(BaseDBTestCase):
    def test_crud(self):
        female = Gender(name='Female')
        male = Gender(name='Male')
        another = Gender(name='Another')
        db.session.add_all([female, male, another])
        db.session.commit()

        self.assertEqual(len(Gender.query.all()), 3)
        self.assertEqual(Gender.query.filter_by(name='Female').first(), female)
        self.assertEqual(Gender.query.filter_by(name='Male').first(), male)
        self.assertEqual(
            Gender.query.filter_by(name='Another').first(), another)

        female.name = 'F'
        male.name = 'M'
        another.name = 'A'
        db.session.commit()

        self.assertEqual(Gender.query.filter_by(name='F').first(), female)
        self.assertEqual(Gender.query.filter_by(name='M').first(), male)
        self.assertEqual(Gender.query.filter_by(name='A').first(), another)

        db.session.delete(female)
        db.session.delete(male)
        db.session.delete(another)
        db.session.commit()

        self.assertFalse(Actor.query.all())


class ActorCrudTestCase(BaseDBTestCase):
    def test_crud(self):
        female = Gender(name='Female')
        male = Gender(name='Male')
        another = Gender(name='Another')
        db.session.add_all([female, male, another])
        db.session.commit()

        actress = Actor(age=23, full_name='Sanjana Sanghi', gender=female)

        actor1 = Actor(age=49, full_name='Saswata Chatterjee', gender=male)

        actor2 = Actor(age=50, full_name='Saif Ali Khan', gender=male)

        db.session.add_all([actress, actor1, actor2])
        db.session.commit()

        self.assertEqual(len(Actor.query.all()), 3)
        self.assertEqual(
            Actor.query.filter_by(full_name='Sanjana Sanghi').first(), actress)
        self.assertEqual(
            Actor.query.filter_by(full_name='Saswata Chatterjee').first(),
            actor1)
        self.assertEqual(
            Actor.query.filter_by(full_name='Saif Ali Khan').first(), actor2)

        self.assertEqual(
            Actor.query.filter_by(
                full_name='Sanjana Sanghi').first().full_name,
            'Sanjana Sanghi')
        self.assertEqual(
            Actor.query.filter_by(
                full_name='Saswata Chatterjee').first().full_name,
            'Saswata Chatterjee')
        self.assertEqual(
            Actor.query.filter_by(full_name='Saif Ali Khan').first().full_name,
            'Saif Ali Khan')

        self.assertEqual(
            Actor.query.filter_by(
                full_name='Sanjana Sanghi').first().gender.name, 'Female')
        self.assertEqual(
            Actor.query.filter_by(
                full_name='Saswata Chatterjee').first().gender.name, 'Male')
        self.assertEqual(
            Actor.query.filter_by(
                full_name='Saif Ali Khan').first().gender.name, 'Male')

        self.assertEqual(
            Actor.query.filter_by(full_name='Sanjana Sanghi').first().age, 23)
        self.assertEqual(
            Actor.query.filter_by(full_name='Saswata Chatterjee').first().age,
            49)
        self.assertEqual(
            Actor.query.filter_by(full_name='Saif Ali Khan').first().age, 50)

        actress.age = 24
        actor1.full_name = 'Saswata ChatterJ'
        actor2.gender = another
        db.session.commit()

        self.assertEqual(
            Actor.query.filter_by(full_name='Sanjana Sanghi').first().age, 24)
        self.assertEqual(
            Actor.query.filter_by(full_name='Saswata ChatterJ').first(),
            actor1)
        self.assertEqual(
            Actor.query.filter_by(
                full_name='Saif Ali Khan').first().gender.name, 'Another')

        db.session.delete(actress)
        db.session.delete(actor1)
        db.session.delete(actor2)
        db.session.commit()

        self.assertFalse(Actor.query.all())

    def get_json_actor(self, *del_args, **replace_kwargs):
        if not Gender.query.all():
            Gender.insert_genders()
        json_actor = {
            'age': 23,
            'fullName': 'Sanjana Sanghi',
            'gender': 'Female'
        }
        for arg in del_args:
            if arg in json_actor:
                del json_actor[arg]
        for k in replace_kwargs:
            json_actor[k] = replace_kwargs[k]
        return json_actor

    def test_can_create_new_from_json(self):
        json_actor = self.get_json_actor()
        actor = Actor.new_from_json(json_actor)
        db.session.commit()

        self.assertIsNotNone(actor)
        self.assertEqual(
            Actor.query.filter_by(uuid=str(actor.uuid)).first().full_name,
            'Sanjana Sanghi')
        self.assertEqual(
            Actor.query.filter_by(uuid=str(actor.uuid)).first().age, 23)
        self.assertEqual(
            Actor.query.filter_by(uuid=str(actor.uuid)).first().gender.name,
            'Female')

    def test_cannot_create_new_from_json(self):
        # test gender is required
        json_actor = self.get_json_actor('gender')
        with self.assertRaises(ValidationsError) as cm:
            Actor.new_from_json(json_actor)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(validation_error.get_error('gender', 'missing_field'))

        # test full_name is required
        json_actor = self.get_json_actor('fullName')
        with self.assertRaises(ValidationsError) as cm:
            Actor.new_from_json(json_actor)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(validation_error.get_error('fullName',
                                                   'missing_field'))

        # test age is required
        json_actor = self.get_json_actor('age')
        with self.assertRaises(ValidationsError) as cm:
            Actor.new_from_json(json_actor)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(validation_error.get_error('age', 'missing_field'))

        # test all required
        json_actor = self.get_json_actor(*{'gender', 'fullName', 'age'})
        with self.assertRaises(ValidationsError) as cm:
            Actor.new_from_json(json_actor)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 3)
        self.assertTrue(validation_error.get_error('gender', 'missing_field'))
        self.assertTrue(validation_error.get_error('fullName',
                                                   'missing_field'))
        self.assertTrue(validation_error.get_error('age', 'missing_field'))

        # test gender not found
        json_actor = self.get_json_actor(gender='F')
        with self.assertRaises(ValidationsError) as cm:
            Actor.new_from_json(json_actor)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(validation_error.get_error('gender', 'unprocessable'))
        self.assertIn(
            'not found',
            validation_error.get_error('gender', 'unprocessable').description)

        # test duplicated movie
        json_actor = self.get_json_actor()
        Actor.new_from_json(json_actor)
        db.session.commit()

        with self.assertRaises(ValidationsError) as cm:
            Actor.new_from_json(json_actor)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(validation_error.get_error('custom', 'already_exists'))
        self.assertIn(
            'already exists',
            validation_error.get_error('custom', 'already_exists').description)

    def add_from_json_actor(self, *del_args, **replace_kwargs):
        json_actor = self.get_json_actor(*del_args, **replace_kwargs)
        actor = Actor.new_from_json(json_actor)
        db.session.commit()
        return actor

    def test_can_update_from_json(self):
        actor = self.add_from_json_actor()

        # update all attributes
        json_actor = actor.to_json()
        json_actor['fullName'] = 'Sanjana Sanghi Jr.'
        json_actor['age'] = 24
        json_actor['gender'] = 'Another'
        actor.update_from_json(json_actor)
        db.session.commit()
        self.assertEqual(
            Actor.query.filter_by(uuid=json_actor['uuid']).first().full_name,
            'Sanjana Sanghi Jr.')
        self.assertEqual(
            Actor.query.filter_by(uuid=json_actor['uuid']).first().age, 24)
        self.assertEqual(
            Actor.query.filter_by(uuid=json_actor['uuid']).first().gender.name,
            'Another')

        # update full_name attributes
        actor.update_from_json({'fullName': 'Sanjana S. Junior'})
        db.session.commit()
        self.assertEqual(
            Actor.query.filter_by(uuid=json_actor['uuid']).first().full_name,
            'Sanjana S. Junior')
        self.assertEqual(
            Actor.query.filter_by(uuid=json_actor['uuid']).first().age, 24)
        self.assertEqual(
            Actor.query.filter_by(uuid=json_actor['uuid']).first().gender.name,
            'Another')

        # update age attributes
        actor.update_from_json({'age': 30})
        db.session.commit()
        self.assertEqual(
            Actor.query.filter_by(uuid=json_actor['uuid']).first().full_name,
            'Sanjana S. Junior')
        self.assertEqual(
            Actor.query.filter_by(uuid=json_actor['uuid']).first().age, 30)
        self.assertEqual(
            Actor.query.filter_by(uuid=json_actor['uuid']).first().gender.name,
            'Another')

        # update gender attributes
        actor.update_from_json({'gender': 'Female'})
        db.session.commit()
        self.assertEqual(
            Actor.query.filter_by(uuid=json_actor['uuid']).first().full_name,
            'Sanjana S. Junior')
        self.assertEqual(
            Actor.query.filter_by(uuid=json_actor['uuid']).first().age, 30)
        self.assertEqual(
            Actor.query.filter_by(uuid=json_actor['uuid']).first().gender.name,
            'Female')

    def test_cannot_update_from_json(self):
        actor = self.add_from_json_actor()

        # test gender not found
        json_actor = actor.to_json()
        json_actor['gender'] = 'F'
        with self.assertRaises(ValidationsError) as cm:
            actor.update_from_json(json_actor)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(validation_error.get_error('gender', 'unprocessable'))
        self.assertIn(
            'not found',
            validation_error.get_error('gender', 'unprocessable').description)

        # test duplicated actor
        self.add_from_json_actor(fullName='Sanjana Sanghi Jr.')
        json_movie = actor.to_json()
        json_movie['fullName'] = 'Sanjana Sanghi Jr.'
        with self.assertRaises(ValidationsError) as cm:
            actor.update_from_json(json_movie)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(validation_error.get_error('custom', 'already_exists'))
        self.assertIn(
            'already exists',
            validation_error.get_error('custom', 'already_exists').description)


class MovieCrudTestCase(BaseDBTestCase):
    def test_crud(self):
        female = Gender(name='Female')
        male = Gender(name='Male')
        another = Gender(name='Another')
        db.session.add_all([female, male, another])
        db.session.commit()

        actress = Actor(age=23, full_name='Sanjana Sanghi', gender=female)

        actor1 = Actor(age=49, full_name='Saswata Chatterjee', gender=male)

        actor2 = Actor(age=49, full_name='Saif Ali Khan', gender=male)

        db.session.add_all([actress, actor1, actor2])
        db.session.commit()

        movie = Movie(title='Dil Bechara',
                      release_date=datetime(2020, 7, 24),
                      actors=[actress, actor1, actor2])
        db.session.add(movie)
        db.session.commit()

        self.assertEqual(len(Movie.query.all()), 1)
        self.assertEqual(
            Movie.query.filter_by(title='Dil Bechara').first(), movie)
        self.assertEqual(
            Movie.query.filter_by(title='Dil Bechara').first().release_date,
            datetime(2020, 7, 24).date())
        self.assertListEqual([
            a.full_name
            for a in Movie.query.filter_by(title='Dil Bechara').first().actors
        ], ['Sanjana Sanghi', 'Saswata Chatterjee', 'Saif Ali Khan'])

        movie.release_date = datetime(2020, 7, 31)
        db.session.commit()

        self.assertEqual(
            Movie.query.filter_by(title='Dil Bechara').first().release_date,
            datetime(2020, 7, 31).date())

        db.session.delete(movie)
        db.session.commit()

        self.assertFalse(Movie.query.all())

    def get_json_movie(self, *del_args, **replace_kwargs):
        if not Gender.query.all():
            Gender.insert_genders()

        actors = Actor.query.all()
        if not actors:
            actors = [
                Actor(age=23,
                      full_name='Sanjana Sanghi',
                      gender=Gender.query.filter_by(name='Female').first()),
                Actor(age=49,
                      full_name='Saswata Chatterjee',
                      gender=Gender.query.filter_by(name='Male').first()),
                Actor(age=49,
                      full_name='Saif Ali Khan',
                      gender=Gender.query.filter_by(name='Male').first())
            ]
            db.session.add_all(actors)
            db.session.commit()
        json_movie = {
            'title': 'Dil Bechara',
            'releaseDate': '2020-07-24',
            'actors': [a.to_json() for a in actors]
        }
        for arg in del_args:
            if arg in json_movie:
                del json_movie[arg]
        for k in replace_kwargs:
            json_movie[k] = replace_kwargs[k]
        return json_movie

    def test_can_create_new_from_json(self):
        json_movie = self.get_json_movie()

        movie = Movie.new_from_json(json_movie)
        db.session.commit()
        self.assertIsNotNone(movie)
        self.assertEqual(
            Movie.query.filter_by(uuid=str(movie.uuid)).first().title,
            'Dil Bechara')
        self.assertEqual(
            date_to_str(
                Movie.query.filter_by(
                    uuid=str(movie.uuid)).first().release_date), '2020-07-24')
        self.assertEqual(
            len(
                Movie.query.filter_by(
                    uuid=str(movie.uuid)).first().actors.all()), 3)
        self.assertListEqual([
            a.full_name for a in Movie.query.filter_by(
                uuid=str(movie.uuid)).first().actors.all()
        ], ['Sanjana Sanghi', 'Saswata Chatterjee', 'Saif Ali Khan'])

    def test_cannot_create_new_from_json(self):
        # test title is required
        json_movie = self.get_json_movie('title')
        with self.assertRaises(ValidationsError) as cm:
            Movie.new_from_json(json_movie)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(validation_error.get_error('title', 'missing_field'))

        # test release_date is required
        json_movie = self.get_json_movie('releaseDate')
        with self.assertRaises(ValidationsError) as cm:
            Movie.new_from_json(json_movie)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(
            validation_error.get_error('releaseDate', 'missing_field'))

        # test actors is required
        json_movie = self.get_json_movie('actors')
        with self.assertRaises(ValidationsError) as cm:
            Movie.new_from_json(json_movie)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(validation_error.get_error('actors', 'missing_field'))

        # test all required
        json_movie = self.get_json_movie(*{'title', 'releaseDate', 'actors'})
        with self.assertRaises(ValidationsError) as cm:
            Movie.new_from_json(json_movie)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 3)
        self.assertTrue(validation_error.get_error('title', 'missing_field'))
        self.assertTrue(
            validation_error.get_error('releaseDate', 'missing_field'))
        self.assertTrue(validation_error.get_error('actors', 'missing_field'))

        # test actors is a list and all have uuid
        json_movie = self.get_json_movie()
        json_movie['actors'] = [{k: v
                                 for k, v in a.items() if k != 'uuid'}
                                for a in json_movie['actors']]
        with self.assertRaises(ValidationsError) as cm:
            Movie.new_from_json(json_movie)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(validation_error.get_error('actors', 'missing_field'))
        self.assertIn(
            'uuid',
            validation_error.get_error('actors', 'missing_field').description)

        # test valid release date
        json_movie = self.get_json_movie(releaseDate='16/08/2020')
        with self.assertRaises(ValidationsError) as cm:
            Movie.new_from_json(json_movie)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(validation_error.get_error('releaseDate', 'invalid'))
        self.assertIn(
            f'you must use date with format: {date_to_str(now())}',
            validation_error.get_error('releaseDate', 'invalid').description)

        # test actor not found
        json_movie = self.get_json_movie()
        json_movie['actors'] = [{
            k: v if k != 'uuid' else str(uuid.uuid4())
            for k, v in a.items()
        } for a in json_movie['actors']]
        with self.assertRaises(ValidationsError) as cm:
            Movie.new_from_json(json_movie)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(validation_error.get_error('actors', 'unprocessable'))
        self.assertIn(
            'not found',
            validation_error.get_error('actors', 'unprocessable').description)

        # test duplicated movie
        json_movie = self.get_json_movie()
        Movie.new_from_json(json_movie)
        db.session.commit()

        with self.assertRaises(ValidationsError) as cm:
            Movie.new_from_json(json_movie)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(validation_error.get_error('custom', 'already_exists'))
        self.assertIn(
            'already exists',
            validation_error.get_error('custom', 'already_exists').description)

    def add_from_json_movie(self, *del_args, **replace_kwargs):
        json_movie = self.get_json_movie(*del_args, **replace_kwargs)
        movie = Movie.new_from_json(json_movie)
        db.session.commit()
        return movie

    def test_can_update_from_json(self):
        movie = self.add_from_json_movie()

        # update all attributes
        json_movie = movie.to_json()
        json_movie['title'] = 'Dil Bechara 2'
        json_movie['releaseDate'] = '2020-07-31'
        json_movie['actors'] = [
            movie.actors.filter_by(
                full_name='Sanjana Sanghi').first().to_json()
        ]
        movie.update_from_json(json_movie)
        db.session.commit()
        self.assertEqual(
            Movie.query.filter_by(uuid=json_movie['uuid']).first().title,
            'Dil Bechara 2')
        self.assertEqual(
            date_to_str(
                Movie.query.filter_by(
                    uuid=json_movie['uuid']).first().release_date),
            '2020-07-31')
        self.assertEqual(
            len(
                Movie.query.filter_by(
                    uuid=json_movie['uuid']).first().actors.all()), 1)
        self.assertListEqual([
            a.full_name for a in Movie.query.filter_by(
                uuid=json_movie['uuid']).first().actors.all()
        ], ['Sanjana Sanghi'])

        # update title attributes
        movie.update_from_json({'title': 'Dil Bechara'})
        db.session.commit()
        self.assertEqual(
            Movie.query.filter_by(uuid=json_movie['uuid']).first().title,
            'Dil Bechara')
        self.assertEqual(
            date_to_str(
                Movie.query.filter_by(
                    uuid=json_movie['uuid']).first().release_date),
            '2020-07-31')
        self.assertEqual(
            len(
                Movie.query.filter_by(
                    uuid=json_movie['uuid']).first().actors.all()), 1)
        self.assertListEqual([
            a.full_name for a in Movie.query.filter_by(
                uuid=json_movie['uuid']).first().actors.all()
        ], ['Sanjana Sanghi'])

        # update release_date attributes
        movie.update_from_json({'releaseDate': '2020-07-24'})
        db.session.commit()
        self.assertEqual(
            Movie.query.filter_by(uuid=json_movie['uuid']).first().title,
            'Dil Bechara')
        self.assertEqual(
            date_to_str(
                Movie.query.filter_by(
                    uuid=json_movie['uuid']).first().release_date),
            '2020-07-24')
        self.assertEqual(
            len(
                Movie.query.filter_by(
                    uuid=json_movie['uuid']).first().actors.all()), 1)
        self.assertListEqual([
            a.full_name for a in Movie.query.filter_by(
                uuid=json_movie['uuid']).first().actors.all()
        ], ['Sanjana Sanghi'])

        # update actors attributes
        movie.update_from_json({
            'actors': [
                Actor.query.filter_by(
                    full_name='Saif Ali Khan').first().to_json()
            ]
        })
        db.session.commit()
        self.assertEqual(
            Movie.query.filter_by(uuid=json_movie['uuid']).first().title,
            'Dil Bechara')
        self.assertEqual(
            date_to_str(
                Movie.query.filter_by(
                    uuid=json_movie['uuid']).first().release_date),
            '2020-07-24')
        self.assertEqual(
            len(
                Movie.query.filter_by(
                    uuid=json_movie['uuid']).first().actors.all()), 1)
        self.assertListEqual([
            a.full_name for a in Movie.query.filter_by(
                uuid=json_movie['uuid']).first().actors.all()
        ], ['Saif Ali Khan'])

    def test_cannot_update_from_json(self):
        movie = self.add_from_json_movie()

        # test valid release date
        json_movie = movie.to_json()
        json_movie['releaseDate'] = '31-07-2020'
        with self.assertRaises(ValidationsError) as cm:
            movie.update_from_json(json_movie)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(validation_error.get_error('releaseDate', 'invalid'))
        self.assertIn(
            f'you must use date with format: {date_to_str(now())}',
            validation_error.get_error('releaseDate', 'invalid').description)

        # test actors is a list and all have uuid
        json_movie = movie.to_json()
        json_movie['actors'] = [{k: v
                                 for k, v in a.items() if k != 'uuid'}
                                for a in json_movie['actors']]
        with self.assertRaises(ValidationsError) as cm:
            movie.update_from_json(json_movie)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(validation_error.get_error('actors', 'missing_field'))
        self.assertIn(
            'uuid',
            validation_error.get_error('actors', 'missing_field').description)

        # test actor not found
        json_movie = movie.to_json()
        json_movie['actors'] = [{
            k: v if k != 'uuid' else str(uuid.uuid4())
            for k, v in a.items()
        } for a in json_movie['actors']]
        with self.assertRaises(ValidationsError) as cm:
            movie.update_from_json(json_movie)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(validation_error.get_error('actors', 'unprocessable'))
        self.assertIn(
            'not found',
            validation_error.get_error('actors', 'unprocessable').description)

        # test duplicated movie
        self.add_from_json_movie(title='Dil Bechara 2')
        json_movie = movie.to_json()
        json_movie['title'] = 'Dil Bechara 2'
        with self.assertRaises(ValidationsError) as cm:
            movie.update_from_json(json_movie)
        validation_error = cm.exception
        self.assertTrue(validation_error.has_errors())
        self.assertTrue(len(validation_error.errors), 1)
        self.assertTrue(validation_error.get_error('custom', 'already_exists'))
        self.assertIn(
            'already exists',
            validation_error.get_error('custom', 'already_exists').description)


if __name__ == '__main__':
    unittest.main()
