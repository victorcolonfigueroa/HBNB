from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app, version='1.0', title='User Management API',
          description='A simple User Management API')

from api import user_routes, country_city_routes
api.add_namespace(user_routes.ns_user)
api.add_namespace(country_city_routes.ns_country)
api.add_namespace(country_city_routes.ns_city)

