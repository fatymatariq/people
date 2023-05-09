# config.py

import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from people_api.constants import API_CONFIG_FILE, BASE_DIR

db = SQLAlchemy()
ma = Marshmallow()

def create_app(database_uri):
    connex_app = connexion.App(__name__, specification_dir=BASE_DIR)
    connex_app.add_api(f"{BASE_DIR / API_CONFIG_FILE}")

    app = connex_app.app
    app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    ma.init_app(app)

    return connex_app
