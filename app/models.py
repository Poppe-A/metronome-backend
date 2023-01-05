from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from app.db_init import db, ma

user_sport = db.Table('user_sport',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('sport_id', db.Integer, db.ForeignKey('sport.id'))
)

class Sport(db.Model,):
    __tablename__ = "sport"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f'Sport(name={self.name})'

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    #sessions = db.relationship('Session', backref='user')
    sports = db.relationship('Sport', secondary=user_sport, backref='sports')
    
    def __init__(self, name, password):
        self.name = name
        self.password = password



class Session(db.Model):
    __tablename__ = "session"

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    name = ma.auto_field()
    password = ma.auto_field()
    #sessions = ma.auto_field()

class SessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Session
        include_fk = True