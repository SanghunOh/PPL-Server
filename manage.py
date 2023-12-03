import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/app')

from flask import flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.main import create_app, db

# @app.before_first_request
# def create_tables():
#     db.create_all()

app = create_app('dev')

@app.before_first_request
def create_tables():
    db.create_all()

app.register_blueprint(blueprint)

app.app_context().push()

@manager.command
def run():
    app.run(host='0.0.0.0')