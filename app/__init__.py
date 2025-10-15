#where I create the create_app function
from flask import Flask
from .models import db
from .extensions import ma
from .blueprints.users import users_bp
from .blueprints.collections import collections_bp

#create the application factory
def create_app(config_name):

    #initialze blank app
    app = Flask(__name__)
    #configure the app
    app.config.from_object(f'config.{config_name}')

    #Initialize extensions on app
    db.init_app(app)
    ma.init_app(app)

    #plug in blueprints
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(collections_bp, url_prefix='/collections')

    return app