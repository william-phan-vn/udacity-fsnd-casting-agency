import os

from sqlalchemy import Column, String, Integer, DateTime, Enum
from flask_sqlalchemy import SQLAlchemy

database_path = os.getenv('DATABASE_URL')
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
Binds a flask application and SQLAlchemy service
'''
def setup_db(app, path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


class Movies(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False)


class Actors(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(Enum('Male', 'Female', name='gender_types'))

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
