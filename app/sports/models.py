from app.db_init import db, ma
from datetime import datetime

# RELATION TABLES

class Session_Exercise(db.Model):
    __tablename__ = 'session_exercise'
    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(db.ForeignKey('session.id'))
    session = db.relationship("Session", back_populates="exercises")
    exercise_id = db.Column(db.ForeignKey('exercise.id'))
    details = db.Column('details', db.String(50))
    _results = db.Column('results', db.String, default='')
    @property
    def results(self):
        return [float(x) for x in self._results.split(';')]
    @results.setter
    def results(self, results_array):
        print('setter', results_array)
        self._results = ";".join([str(result) for result in results_array])

    @staticmethod 
    def formatResults(str):
        return [float(x) for x in str.split(';')]


# TABLES

class Sport(db.Model):
    __tablename__ = "sport"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    exercises = db.relationship('Exercise', backref='sport')

    def __repr__(self):
        return f'Sport(name={self.name})'


class Session(db.Model):
    __tablename__ = "session"

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.now)
    name = db.Column('name', db.String(30))

    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sport = db.relationship('Sport', backref='sport')

    exercises = db.relationship('Session_Exercise', back_populates="session")

    
class Exercise(db.Model):
    __tablename__ = "exercise"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(30))
    # define unit (reps, time, ...)
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'))


# SCHEMAS

class SportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sport
        include_fk = False


class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        include_fk = True

class SessionExerciseSchema(ma.SQLAlchemyAutoSchema):
    exercise = ma.Nested(ExerciseSchema)

    class Meta:
        model = Session_Exercise
        include_fk = True


class SessionSchema(ma.SQLAlchemyAutoSchema):
    sport = ma.Nested(SportSchema)
    exercises = ma.Nested(SessionExerciseSchema, many=True)

    class Meta:
        model = Session
        include_fk = True