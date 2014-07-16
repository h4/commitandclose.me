from app.models import db
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.mongoengine import MongoEngine
from app.main.views import github
from config import config
from .main import main as main_blueprint


bootstrap = Bootstrap()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    github.init_app(app)
    db.init_app(app)
    app.register_blueprint(main_blueprint)
    return app
