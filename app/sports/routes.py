from flask import Blueprint, jsonify, request
from datetime import datetime
import json

from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.user.models import User
from app.sports.models import Exercise, ExerciseSchema, Session_Exercise, Sport, Session, SessionSchema, SportSchema
from app.db_init import db

sports_routes = Blueprint('sport_routes', __name__, template_folder='templates')

# SPORTS

@sports_routes.route('/all', methods=['GET'])
def get_sports():
    sports = Sport.query.all()
    return jsonify(SportSchema().dump(sports, many=True))


@sports_routes.route('/add', methods=['POST'])
def add_sports():
    data = json.loads(request.data)

    sport = Sport(
        name = data["name"]
    )

    try:
        db.session.add(sport)
        res = db.session.commit()
        return f"{sport.name} added {res}"

    except (SQLAlchemyError, DBAPIError) as e:
        error = str(e.__dict__['orig'])
        return error


@sports_routes.route('/associateSport', methods=['POST'])
@jwt_required()
def associate_sport():
    data = json.loads(request.data)
    current_user = get_jwt_identity()

    if data['user_id'] == current_user["id"]:
        user = User.query.filter(User.id == data['user_id']).one()
        sport = Sport.query.filter(Sport.id == data['sport_id']).one()
        user.sports.append(sport)
        db.session.commit()
        return f"{sport.name} associated to user {data['user_id']}"
    else:
        return 'You cannot associate a sport for this user'


# SESSIONS

@sports_routes.route('/createSession', methods=['POST'])
@jwt_required()
def create_session():
    current_user = get_jwt_identity()
    data = json.loads(request.data)

    session = Session(
        name = data["session_name"],
        user_id = current_user["id"],
        sport_id = data["sport_id"]
    )

    db.session.add(session)
    db.session.commit()

    return "session added"


@sports_routes.route('/sessions', methods=['GET'])
@jwt_required()
def get_sessions():
    current_user = get_jwt_identity()

    sessions = Session.query.filter(Session.user_id == current_user["id"])

    return jsonify(SessionSchema().dump(sessions, many=True))


@sports_routes.route('/sessions/<int:session_id>', methods=['GET'])
@jwt_required()
def get_session(session_id):
    session = Session.query.get(session_id)

    exercises = db.session.query(
        Session_Exercise.details.label('details'), 
        Session_Exercise._results.label('results'), 
        Exercise.name.label('name')) \
    .join(Exercise, Exercise.id == Session_Exercise.exercise_id) \
    .filter(Session_Exercise.session_id == session_id)

    exercises_to_return = map(lambda ex: 
        {**ex, 
        'results': Session_Exercise.formatResults(ex.results)}, 
    exercises)

    session_return = {
        "name": session.name,
        "date": session.created_date,
        "exercises": list(exercises_to_return)
    }

    return session_return


# EXERCISES

@sports_routes.route('/getExercises/<int:sport_id>', methods=['GET'])
def get_exercises(sport_id):
    exercises = Exercise.query.filter(Exercise.sport_id == sport_id)
    return jsonify(ExerciseSchema().dump(exercises, many=True))


@sports_routes.route('/createExercise', methods=['POST'])
def create_exercise():
    data = json.loads(request.data)

    exercise = Exercise(
        name = data["exercise_name"],
        sport_id = data["sport_id"]
    )

    db.session.add(exercise)
    db.session.commit()
    return "Exercise added"


@sports_routes.route('/addExerciseToSession', methods=['POST'])
def add_exercise_to_session():
    data = json.loads(request.data)

    session = Session.query.get(data["session_id"])

    session = Session_Exercise(
        session_id = data["session_id"],
        exercise_id = data["exercise_id"],
        details = data["details"],
        results = data["results"]
    )

    db.session.add(session)
    db.session.commit()

    return "Exercise added"
