from flask import Blueprint, request
from datetime import datetime
import json
from app.user.models import User, UserSchema
from app.db_init import db

user_routes = Blueprint('user_routes', __name__, template_folder='templates')

@user_routes.route("/all")
def all_users():
    user = User.query.all()
    for u in user:
        print('user sports', u.sports)
    return UserSchema().dump(user, many=True)

@user_routes.route("/<int:user_id>")
def user(user_id):
    user = User.query.get_or_404(user_id)
    return UserSchema().dump(user)