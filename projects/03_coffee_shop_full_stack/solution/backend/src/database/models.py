"""
    models.py
    -------

    This module contains the :class:`Drink` class which is responsible for
    holding data about drinks and their recipes.
"""

__author__ = "Filipe Bezerra de Sousa"

import json
import os

from dictalchemy import make_class_dictable
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer

DATABASE_FILENAME = "database.db"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = "sqlite:///{}".format(
    os.path.join(PROJECT_DIR, DATABASE_FILENAME)
)

db = SQLAlchemy()
make_class_dictable(db.Model)


def setup_db(app):
    """Bind a flask application and a SQLAlchemy service.

    :param app: The flask application.
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_PATH
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Drink(db.Model):
    """Drink, a persistent drink entity, extends the base SQLAlchemy Model."""

    __tablename__ = "drinks"

    # Auto incrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required data type is
    # [{'color': string, 'name':string, 'parts':number}]
    recipe = Column(String(180), nullable=False)

    def short(self):
        """Short form representation of the ``Drink`` model.

        :return: A dict with title and only {color, parts} of the recipe.
        """
        short_recipe = [
            {"color": r["color"], "parts": r["parts"]}
            for r in json.loads(self.recipe)
        ]
        return {"id": self.id, "title": self.title, "recipe": short_recipe}

    def long(self):
        """Long form representation of the ``Drink`` model.

        :return: A dict with title and {color, name, parts} of the recipe.
        """
        return {
            "id": self.id,
            "title": self.title,
            "recipe": json.loads(self.recipe),
        }

    def insert(self):
        """Inserts a new ``Drink`` into a database.

        - The model must have a unique ``name``.
        - The model must have a unique ``id`` or null ``id``.

        Example:
            ``drink = Drink(title=req_title, recipe=req_recipe)``

            ``drink.insert()``
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes a ``Drink`` from a database.

        - The model must exist in the database

        Example:
            ``drink = Drink(title=req_title, recipe=req_recipe)``

            ``drink.delete()``
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """Updates a ``Drink`` into a database.

        - The model must exist in the database

        Example:
            ``drink = Drink.query.filter(Drink.id == id).one_or_none()``

            ``drink.title = 'Black Coffee'``

            ``drink.update()``
        """
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())
