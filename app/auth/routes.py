from flask import Blueprint, jsonify, request
from app.db_init import bcrypt, db
from datetime import datetime
import json
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.user.models import User, UserSchema

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
            return jsonify({"message":f"{user.id} created", "status": 201})
        except: 
            return jsonify({"message":"Unable to create user", "status": 500})
    else: 
        return jsonify({"message":"User already exists", "status": 400})


@auth_routes.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)

    user = User.query.filter_by(email=data["email"]).first()

    if user:
        check_password = bcrypt.check_password_hash(user.password , data["password"])
        access_token = create_access_token(identity={"email": data["email"], "id": user.id})
        print('token', access_token)
        if user and check_password:
            return jsonify({"message": "User logged", "jwt": access_token, "status": 200})
    else:
        return jsonify({"message": f"Incorrect credentials", "status": 401})


@auth_routes.route('/currentUser')
@jwt_required()
def getCurrentUser():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@auth_routes.route('/logout')
def logout():
    # logout is probably done in front end by removing jwt
    return f'Logout'

