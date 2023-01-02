from flask import Blueprint, jsonify, request
import json
from app.models import Sport
from app import db

sports_routes = Blueprint('sport_routes', __name__, template_folder='templates')

@sports_routes.route('/', methods=['GET'])
def get_sports():
    sports = Sport.query.all()
    return jsonify(Sport.serialize_list(sports))

@sports_routes.route('/add', methods=['POST'])
def add_sports():
    data = json.loads(request.data)
    print("datra", data)
    sport = Sport(
        name = data["name"]
    )

    db.session.add(sport)
    db.session.commit()

    return f"{sport.name} added"