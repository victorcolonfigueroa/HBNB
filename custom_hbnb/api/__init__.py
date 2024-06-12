from flask import Flask # type: ignore
from flask import Flask  # type: ignore
from .user_routes import setup_routes
from . import amenities_routes
from . import place_routes
from . import reviews_routes



def create_app():
    app = Flask(__name__)
    setup_routes(app)
    return(app)
