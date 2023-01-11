from app.db_init import db, ma
from datetime import datetime


class Sport(db.Model,):
    __tablename__ = "sport"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f'Sport(name={self.name})'

class Session(db.Model):
    __tablename__ = "session"

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class SessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Session
        include_fk = True