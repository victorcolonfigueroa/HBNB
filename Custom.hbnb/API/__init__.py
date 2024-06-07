from flask import Flask # type: ignore
from .user_routes import setup_routes
from .amenities_routes import 


def create_app():
    app = Flask(__name__)
    setup_routes(app)
    return(app)
