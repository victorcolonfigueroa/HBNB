from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app, version='1.0', title='User Management API',
          description='A simple User Management API')

from api import review_routes, user_routes, country_city_routes, amenity_routes, place_routes

api.add_namespace(place_routes.ns_place)
api.add_namespace(user_routes.ns_user)
api.add_namespace(country_city_routes.ns_country_city)
api.add_namespace(amenity_routes.ns_amenity)
api.add_namespace(review_routes.ns_review)
