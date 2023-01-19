from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
import app.config as config
from app.sports.routes import sports_routes
from app.user.routes import user_routes
from app.auth.routes import auth_routes
from app.user.models import *
from app.db_init import db
from flask_jwt_extended import JWTManager



def create_app(test=False):
    app = Flask(__name__)
    app_config = config.TestConfig if test else config.DevConfig
    app.config.from_object(app_config)
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    jwt = JWTManager(app)
        
    db.init_app(app)

    with app.app_context():
        #db.drop_all()
        db.create_all()

    app.register_blueprint(sports_routes, url_prefix='/sports')
    app.register_blueprint(user_routes, url_prefix='/user')
    app.register_blueprint(auth_routes, url_prefix='/auth')

    @app.route('/', methods=['GET'])
    def home():
        return 'Connected to the API - yessouille 5'

    return app            