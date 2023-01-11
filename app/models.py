from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from app.db_init import db, ma
from app.sports import models
user_sport = db.Table('user_sport',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('sport_id', db.Integer, db.ForeignKey('sport.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #sessions = db.relationship('Session', backref='user')
    sports = db.relationship('Sport', secondary=user_sport, backref='sports')

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    name = ma.auto_field()
    password = ma.auto_field()
    #sessions = ma.auto_field()

