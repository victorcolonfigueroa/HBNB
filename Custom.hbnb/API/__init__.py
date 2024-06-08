from flask import Flask # type: ignore
from .user_routes import setup_routes
from .amenities_routes import setup_routes
from passlib import pass #place review here


def create_app():
    app = Flask(__name__)
    setup_routes(app)
    return(app)
