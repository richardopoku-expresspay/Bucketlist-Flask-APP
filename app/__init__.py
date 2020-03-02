from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

db = SQLAlchemy()


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from . import routes

    app.add_url_rule('/bucketlists', methods=['GET', 'POST'], view_func=routes.bucketlists)
    app.add_url_rule('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'], view_func=routes.manipulations)

    return app


