from app.db_init import db, ma
from datetime import datetime

# TABLES

class Song(db.Model):
    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    tempo = db.Column(db.Integer, nullable=False)
    # position = db.Column(db.Integer, unique= True)
    position = db.Column(db.Integer)

    def __repr__(self):
        return f'-name={self.name} -position={self.position}'


# SCHEMAS

class SongSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Song
        include_fk = False