from flask import Flask #type: ignore
from base_model import BaseModel
from countrycls import Country, City
from placescls import Places, Amenities
from reviewscls import Reviews
from usercls import User

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    return app
