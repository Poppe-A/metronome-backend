from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
import app.config as config
from app.songs.routes import songs_routes
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
        # db.drop_all()
        db.create_all()

    app.register_blueprint(songs_routes, url_prefix='/songs')

    @app.route('/', methods=['GET'])
    def home():
        return 'Connected to the API'

    return app            