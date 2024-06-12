from flask import Flask # type: ignore
from .user_routes import setup_routes
import .amenities_routes


def create_app():
    app = Flask(__name__)
    setup_routes(app)
    return(app)
