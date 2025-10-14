#where I create the create_app function
from flask import Flask
from .models import db

#create the application factory
def create_app(config_name):

    #initialze blank app
    app = Flask(__name__)
    #configure the app
    app.config.from_object(f'config.{config_name}')

    #Initialize extensions on app
    db.init_app(app)

    return app