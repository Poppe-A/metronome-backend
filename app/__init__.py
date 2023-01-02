from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from app.models import db, Sport



def create_app(config_class=Config):
    print('--- cool derfgre', __name__ == "__main__")

    app = Flask(__name__)
    app.config.from_object(Config)
    print('test', app.config)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{app.config["DB_USER"]}:{app.config["DB_PASSWORD"]}@{app.config["DB_HOST"]}/{app.config["DB_NAME"]}'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/logme'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@db/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()
    from app.sports.routes import sports_routes

    app.register_blueprint(sports_routes, url_prefix='/sports')

    @app.route('/', methods=['GET'])
    def home():
        return 'cool de f'

    return app            