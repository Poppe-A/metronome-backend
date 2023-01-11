from flask import Blueprint, jsonify, request
from app.db_init import bcrypt, db
from datetime import datetime
import json
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User, UserSchema

auth_routes = Blueprint('auth_routes', __name__, template_folder='templates')

@auth_routes.route('/signup', methods=['POST'])
def signup():
    print("data2")

    data = json.loads(request.data)
    existing_user = User.query.filter_by(email=data["email"]).first()

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')

    if existing_user is None:
        user = User(
            name=data["name"],
            email=data["email"],
            password=hashed_password
        )
        try:
            db.session.add(user)
            db.session.commit()
            #login_user(user)  # Log in as newly created user
            return jsonify({"message":f"{user.id} created", "status": 201})
        except: 
            return jsonify({"message":"Unable to create user", "status": 500})
    else: 
        return jsonify({"message":"User already exists", "status": 400})

@auth_routes.route('/account1')
def test1():
    print('user')
    return jsonify({"data":current_user, "status": 200})

@auth_routes.route('/test')
def testRoute():
    return "ok"

@auth_routes.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)

    user = User.query.filter_by(email=data["email"]).first()
    check_password = bcrypt.check_password_hash(user.password, data["password"])
    
    if user and check_password:
        login_user(user)    
        return jsonify({"message": "User logged", "data": user.id, "status": 200})
    else:
        return jsonify({"message": f"Incorrect credentials {user} - {check_password}", "status": 401})

@auth_routes.route('/logout')
def logout():
    userId = current_user
    logout_user()
    return f'Logout {userId}'

