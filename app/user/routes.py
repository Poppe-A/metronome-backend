from flask import Blueprint, request
from datetime import datetime
import json
from app.models import User, UserSchema
from app.db_init import db

user_routes = Blueprint('user_routes', __name__, template_folder='templates')

@user_routes.route("/all")
def all_users():
    user = User.query.all()
    return UserSchema().dump(user, many=True)

@user_routes.route("/<int:user_id>")
def user(user_id):
    user = User.query.get_or_404(user_id)
    return UserSchema().dump(user)

@user_routes.route('/add', methods=['POST'])
def add_user():
    data = json.loads(request.data)
    user = User(
        name = data["name"],
        password = data["password"]
    )

    db.session.add(user)
    db.session.commit()

    return UserSchema().dump(user)