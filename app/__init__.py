import config

from flask import Flask
from flask import Blueprint
from flask_restx import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.service.MakeDB import run as model_run

db = SQLAlchemy()
migrate = Migrate()

modeldata = model_run();
# modeldata = {}

from app.controller.user_controller import api as user_api
from app.controller.model_controller import api as model_api

from app.model import user


def get_user_blueprint():
    blueprint = Blueprint('user', __name__, url_prefix='/user')
    api = Api(blueprint, title='ppl_user', version='1.0', description='')
    api.add_namespace(user_api)
    return blueprint

def get_model_blueprint():
    blueprint = Blueprint('model', __name__, url_prefix='/model')
    api = Api(blueprint, title='ppl_user', version='1.0', description='')
    api.add_namespace(model_api)
    return blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(get_user_blueprint())
    app.register_blueprint(get_model_blueprint())

    return app