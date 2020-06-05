import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

DATABASE_NAME = os.getenv("DB_NAME")
DATABASE_USER = os.getenv("DB_USER")
DATABASE_HOST = os.getenv("DB_HOST")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE_PATH = f'postgresql://{DATABASE_USER}:\
    {DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'

db = SQLAlchemy()


def setup_db(app, database_uri=DATABASE_PATH):
    """Bind a flask application and a SQLAlchemy service"""
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Question(db.Model):
    """Question model class."""

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "category": self.category,
            "difficulty": self.difficulty,
        }


class Category(db.Model):
    """Category model class."""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {"id": self.id, "type": self.type}
