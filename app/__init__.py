from flask import Flask
from flask_login import LoginManager
import os
from flask_sqlalchemy import SQLAlchemy
import app.config as config
from app.sports.routes import sports_routes
from app.user.routes import user_routes
from app.auth.routes import auth_routes
from app.models import *
from app.db_init import db



def create_app(test=False):
    app = Flask(__name__)
    app_config = config.TestConfig if test else config.DevConfig
    app.config.from_object(app_config)

    if test:
        app.config["LOGIN_DISABLED"] = True
        
    db.init_app(app)

    with app.app_context():
        #db.drop_all()
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)
    


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(sports_routes, url_prefix='/sports')
    app.register_blueprint(user_routes, url_prefix='/user')
    app.register_blueprint(auth_routes, url_prefix='/auth')

    @app.route('/', methods=['GET'])
    def home():
        return 'Connected to the API - ye'

    return app            