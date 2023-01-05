from flask import Blueprint, jsonify, request
from datetime import datetime
import json
from app.models import User, UserSchema
from app import db

user_routes = Blueprint('user_routes', __name__, template_folder='templates')

@user_routes.route("/<int:user_id>")
def user(user_id):
    user = User.query.get_or_404(user_id)
    #print("user", User.serialize(user))
    print("user", user)
    print("user", user.name)
    return UserSchema().dump(user)

@user_routes.route('/add', methods=['POST'])
def add_user():
    data = json.loads(request.data)
    print("data", data)
    user = User(
        name = data["name"],
        password = data["password"]
    )

    db.session.add(user)
    db.session.commit()

    print("user", user)
    print("user", user.name)
    return UserSchema().dump(user)