"""Classes responsible for holding data and performing intrinsic validations.

    Actor.new_from_json(): Create a new instance of an Actor from json data.
    Movie.new_from_json(): Create a new instance of an Movie from json data
"""

__author__ = "Filipe Bezerra de Sousa"

import uuid
from sqlalchemy.orm import exc
from sqlalchemy_utils import UUIDType
from app import db
from app.date import date_to_str, now, str_to_date
from app.exceptions import ValidationsError


class UUIDSupportModel(db.Model):
    """Mixin model to support a UUID column.
    It declares either a `ID` column as primary key and a `uuid` column as a 
    string default to `uuid.uuid4`.
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        UUIDType(binary=False),
        nullable=False,
        unique=True,
        default=uuid.uuid4)

    def __eq__(self, other):
        """Compare two instances of a model using their `ID` column.
        
        :param other: The other instance of a mode to compare to.
        :return: True if both are equal, False otherwise.
        """
        if isinstance(other, type(self)):
            return self.id == other.id


class Gender(UUIDSupportModel, db.Model):
    """Gender model, a persistent entity which extends the base SQLAlchemy Model.

    Each instances of a gender is associated with a Actor instance.
    """
    __tablename__ = 'genders'
    name = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        """Simple string representation of a gender instance.

        :return: The string representation of this gender.
        """
        return f'<Gender {self.name}>'

    @staticmethod
    def insert_genders():
        """Populate `genders` table with predefined data."""
        genders = [
            Gender(name='Female'),
            Gender(name='Male'),
            Gender(name='Another')
        ]
        for gender in genders:
            found = Gender.query.filter_by(name=gender.name).first()
            if found is None:
                db.session.add(gender)
        db.session.commit()


movies_actors = db.Table(
    'movies_actors',
    db.Column(
        'movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column(
        'actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True))


class Actor(UUIDSupportModel, db.Model):
    """Actor model, a persistent entity which extends the base SQLAlchemy Model.

    Many instances of a actor could be associated with a Movie instance.
    """
    __tablename__ = 'actors'
    age = db.Column(db.Integer)
    full_name = db.Column(db.String(60), nullable=False)
    gender = db.relationship('Gender', uselist=False)
    gender_id = db.Column(
        db.Integer, db.ForeignKey('genders.id'), nullable=False)

    def __repr__(self):
        """Simple string representation of a actor instance.

        :return: The string representation of this actor.
        """
        return f'<Actor {self.full_name}>'

    def to_json(self):
        """Convert this actor instance into a flat dict format.

        :return: A dict containing only specific properties of an actor.
        """
        return {
            'age': self.age,
            'fullName': self.full_name,
            'gender': self.gender.name,
            'moviesCount': self.movies.count(),
            'uuid': str(self.uuid)
        }

    def update_from_json(self, json_actor):
        """Take this instance and update it with new data.

        May raise several validation errors through a
        :class:`exceptions.ValidationsError` exception.

        :param json_actor: A dict containing the new data.
        """
        validation = ValidationsError('Validation failed')
        if not json_actor:
            validation.add_error(
                'all', 'missing_field',
                'you must provide at least age, fullName or gender')
            raise validation

        gender_name = json_actor.get('gender')
        full_name = json_actor.get('fullName')
        age = json_actor.get('age')

        gender = None
        # validation: gender not found
        if gender_name and gender_name != self.gender.name:
            gender = Gender.query.filter_by(name=gender_name).first()
            if not gender:
                validation.add_error(
                    'gender', 'unprocessable', 'gender not found')

        # validation: duplicated, same name, age and gender
        if full_name:
            filter_full_name = full_name or self.full_name
            filter_age = age or self.age
            filter_gender = gender_name or self.gender.name
            actor_found = Actor.query.filter_by(
                full_name=filter_full_name, age=filter_age).join(
                    Gender,
                    Actor.gender).filter(Gender.name == filter_gender).first()
            if actor_found:
                validation.add_error(
                    'custom', 'already_exists',
                    f'actor {full_name} already exists')

        if validation.has_errors():
            raise validation
        if full_name:
            self.full_name = full_name
        if age:
            self.age = age
        if gender:
            self.gender = gender

    @staticmethod
    def new_from_json(json_actor):
        """Create a new instance and assign it new data.

        May raise several validation errors through a
        :class:`exceptions.ValidationsError` exception.

        :param json_actor: A dict containing the new data.
        :raises ValidationsError: If some constraint is violated.
        :return: A new instance of :class:`Actor`.
        """
        gender_name = json_actor.get('gender')
        full_name = json_actor.get('fullName')
        age = json_actor.get('age')

        validation = ValidationsError('Validation failed')
        # validate required attributes
        if not age:
            validation.add_error(
                'age', 'missing_field', 'field age is required')
        if not full_name:
            validation.add_error(
                'fullName', 'missing_field', 'field full name is required')
        if not gender_name:
            validation.add_error(
                'gender', 'missing_field', 'field gender is required')

        gender = None
        if not validation.has_errors():
            gender = Gender.query.filter_by(name=gender_name).first()

            # validation: gender not found
            if not gender:
                validation.add_error(
                    'gender', 'unprocessable', 'gender not found')

            # validation: duplicated, same name, age and gender
            actor_found = Actor.query.filter_by(
                full_name=full_name, age=age).join(
                    Gender,
                    Actor.gender).filter(Gender.name == gender_name).first()
            if actor_found:
                validation.add_error(
                    'custom', 'already_exists',
                    f'actor {full_name} already exists')

        if validation.has_errors():
            raise validation
        actor = Actor(age=age, full_name=full_name, gender=gender)
        db.session.add(actor)
        return actor


class Movie(UUIDSupportModel, db.Model):
    """Movie model, a persistent entity which extends the base SQLAlchemy Model.

    Each instance of a movie associates many instances of actors.
    """
    __tablename__ = 'movies'
    title = db.Column(db.String(140), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    actors = db.relationship(
        'Actor',
        secondary=movies_actors,
        backref=db.backref('movies', lazy='dynamic'),
        lazy='dynamic')

    def __repr__(self):
        """Simple string representation of a movie instance.

        :return: The string representation of this movie.
        """
        return f'<Movie {self.title}>'

    def to_json(self):
        """Convert this movie instance into a flat dict format.

        :return A flat dict containing only specific properties of a movie.
        """
        return {
            'actors': [actor.to_json() for actor in self.actors],
            'releaseDate': date_to_str(self.release_date),
            'title': self.title,
            'uuid': str(self.uuid)
        }

    def update_from_json(self, json_movie):
        """Take this instance and update it with new data.

        May raise several validation errors through a
        :class:`exceptions.ValidationsError` exception.

        :param json_actor: A dict containing the new data.
        """
        validation = ValidationsError('Validation failed')
        if not json_movie:
            validation.add_error(
                'all', 'missing_field',
                'you must provide at least title, releaseDate or actors')
            raise validation

        title = json_movie.get('title')
        release_date_string = json_movie.get('releaseDate')
        actors_json = json_movie.get('actors')

        release_date = str_to_date(release_date_string) \
            if release_date_string else None
        if release_date_string and not release_date:
            validation.add_error(
                'releaseDate', 'invalid',
                f'you must use date with format: {date_to_str(now())}')
        # validation: actor not found
        actors = []
        if actors_json and not (isinstance(actors_json, list)
                                and all([item.get('uuid')
                                         for item in actors_json])):
            validation.add_error(
                'actors', 'missing_field', 'each actor must have uuid')
        elif actors_json:
            for a in actors_json:
                try:
                    actors.append(Actor.query.filter_by(uuid=a['uuid']).one())
                except exc.NoResultFound:
                    validation.add_error(
                        'actors', 'unprocessable',
                        f'actor {a["uuid"]} not found')
        # validate duplicated: title and release_date
        movie_found = None
        if title or release_date_string:
            filter_title = title or self.title
            filter_release_date = release_date_string or str(self.release_date)
            movie_found = Movie.query.filter_by(
                title=filter_title, release_date=filter_release_date).first()
        if movie_found:
            validation.add_error(
                'custom', 'already_exists', f'movie {title} '
                f'released {release_date} '
                f'already exists')
        if validation.has_errors():
            raise validation
        if title:
            self.title = title
        if release_date:
            self.release_date = release_date
        if actors:
            self.actors = actors

    @staticmethod
    def new_from_json(json_movie):
        """Create a new instance and assign it new data.

        May raise several validation errors through a
        :class:`exceptions.ValidationsError` exception.

        :param json_actor: A dict containing the new data.
        :raises ValidationsError: If some constraint is violated.
        :return: A new instance of :class:`Movie`.
        """
        title = json_movie.get('title')
        release_date_string = json_movie.get('releaseDate')
        actors_json = json_movie.get('actors')

        release_date = None
        actors = []

        validation = ValidationsError('Validation failed')
        # validate required attributes
        if not title:
            validation.add_error(
                'title', 'missing_field', 'field title is required')
        if not release_date_string:
            validation.add_error(
                'releaseDate', 'missing_field',
                'field release date is required')
        if not actors_json:
            validation.add_error(
                'actors', 'missing_field', 'field actors is required')
        elif not (isinstance(actors_json, list)
                  and all([item.get('uuid') for item in actors_json])):
            validation.add_error(
                'actors', 'missing_field', 'each actor must have uuid')

        if not validation.has_errors():
            # validate: valid release_date
            release_date = str_to_date(release_date_string)

            if not release_date:
                validation.add_error(
                    'releaseDate', 'invalid',
                    f'you must use date with format: {date_to_str(now())}')

            # validation: actor not found
            if actors_json:
                for a in actors_json:
                    try:
                        actors.append(
                            Actor.query.filter_by(uuid=a['uuid']).one())
                    except exc.NoResultFound:
                        validation.add_error(
                            'actors', 'unprocessable',
                            f'actor {a["uuid"]} not found')

            # validate duplicated: title and release_date
            movie_found = Movie.query.filter_by(
                title=title, release_date=release_date_string).first()
            if movie_found:
                validation.add_error(
                    'custom', 'already_exists',
                    f'movie {title} released {release_date} '
                    f'already exists')

        if validation.has_errors():
            raise validation
        movie = Movie(title=title, release_date=release_date, actors=actors)
        db.session.add(movie)
        return movie
