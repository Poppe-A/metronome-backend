from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect

db = SQLAlchemy()


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class Sport(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def serialize(self):
        d = Serializer.serialize(self)
        return d
        
    def __repr__(self):
        return f'Sport(name={self.name})'