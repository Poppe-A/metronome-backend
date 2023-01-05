from flask import Blueprint, jsonify, request
from datetime import datetime
import json
from app.models import Sport, Session, SessionSchema, User
from app import db

sports_routes = Blueprint('sport_routes', __name__, template_folder='templates')

@sports_routes.route('/', methods=['GET'])
def get_sports():
    sports = Sport.query.all()
    return jsonify(SessionSchema().dump(sports, many=True))

@sports_routes.route('/add', methods=['POST'])
def add_sports():
    data = json.loads(request.data)
    print("data", data)
    sport = Sport(
        name = data["name"]
    )

    db.session.add(sport)
    db.session.commit()

    return f"{sport.name} added"

@sports_routes.route('/associateSport', methods=['POST'])
def associate_sport():
    data = json.loads(request.data)
    user = User.query.filter(User.id == data['user_id']).one()
    sport = Sport.query.filter(Sport.id == data['sport_id']).one()
    user.sports.append(sport)
    db.session.commit()

    return f"{sport.name} added"

@sports_routes.route('/addSession', methods=['POST'])
def add_session():
    data = json.loads(request.data)
    print("data", data)
    session = Session(
        user_id = data["user_id"]
    )

    db.session.add(session)
    db.session.commit()

    return "session added"

@sports_routes.route('/sessions', methods=['GET'])
def get_sessions():
    sessions = Session.query.filter(Session.user_id == "1")
    for session in sessions:
        print("aaaa", session)
    print('session', sessions)
    #print('sosos', SessionSchema().dump(sessions, many=True))
    return jsonify(SessionSchema().dump(sessions, many=True))