from flask import request, abort
from flask_restx import Namespace, Resource, fields
from model.countrycls import Country, City

ns_country_city = Namespace('country_city', description='Country and City operations')

country_model = ns_country_city.model('Country', {
    'id': fields.String(readOnly=True, description='The unique identifier of a country'),
    'name': fields.String(required=True, description='The country name'),
    'code': fields.String(required=True, description='The country code'),
    'created_at': fields.DateTime(readOnly=True, description='The date and time the country was created'),
    'updated_at': fields.DateTime(readOnly=True, description='The date and time the country was last updated'),
    'cities': fields.List(fields.Nested(ns_country_city.model('City', {
        'id': fields.String(readOnly=True, description='The unique identifier of a city'),
        'name': fields.String(required=True, description='The city name'),
        'country_id': fields.String(required=True, description='The country ID'),
        'created_at': fields.DateTime(readOnly=True, description='The date and time the city was created'),
        'updated_at': fields.DateTime(readOnly=True, description='The date and time the city was last updated')
    })))
})

city_model = ns_country_city.model('City', {
    'id': fields.String(readOnly=True, description='The unique identifier of a city'),
    'name': fields.String(required=True, description='The city name'),
    'country_id': fields.String(required=True, description='The country ID'),
    'created_at': fields.DateTime(readOnly=True, description='The date and time the city was created'),
    'updated_at': fields.DateTime(readOnly=True, description='The date and time the city was last updated')
})

def validate_city_data(data):
    if 'name' not in data or not isinstance(data['name'], str) or not data['name'].strip():
        abort(400, description="City name must be a non-empty string")
    if 'country_id' not in data or not isinstance(data['country_id'], str):
        abort(400, description="Country ID must be provided and must be a string")
    country = Country.load(data['country_id'])
    if not country:
        abort(400, description="Invalid country ID")

@ns_country_city.route('/countries')
class CountryList(Resource):
    @ns_country_city.doc('list_countries')
    @ns_country_city.marshal_list_with(country_model)
    def get(self):
        countries = Country.load_all()
        return [country.to_dict() for country in countries]

    @ns_country_city.doc('create_country')
    @ns_country_city.expect(country_model)
    @ns_country_city.marshal_with(country_model, code=201)
    def post(self):
        if not request.json:
            abort(400, description="Request payload must be JSON")
        data = request.json
        country = Country(
            name=data['name'],
            code=data['code']
        )
        return country.to_dict(), 201

@ns_country_city.route('/countries/<string:country_id>')
@ns_country_city.response(404, 'Country not found')
@ns_country_city.param('country_id', 'The country identifier')
class CountryResource(Resource):
    @ns_country_city.doc('get_country')
    @ns_country_city.marshal_with(country_model)
    def get(self, country_id):
        country = Country.load(country_id)
        if not country:
            abort(404, description="Country not found")
        return country.to_dict()

@ns_country_city.route('/countries/<string:country_id>/cities')
@ns_country_city.response(404, 'Country not found')
@ns_country_city.param('country_id', 'The country identifier')
class CountryCityList(Resource):
    @ns_country_city.doc('list_cities_for_country')
    @ns_country_city.marshal_list_with(city_model)
    def get(self, country_id):
        country = Country.load(country_id)
        if not country:
            abort(404, description="Country not found")
        cities = [City.load(city_id) for city_id in country.cities]
        return [city.to_dict() for city in country.cities]

    @ns_country_city.doc('create_city_for_country')
    @ns_country_city.expect(city_model)
    @ns_country_city.marshal_with(city_model, code=201)
    def post(self, country_id):
        if not request.json:
            abort(400, description="Request payload must be JSON")
        data = request.json
        data['country_id'] = country_id
        validate_city_data(data)
        city = City(
            name=data['name'],
            country_id=data['country_id']
        )
        country = Country.load(country_id)
        country.add_city(city)
        return city.to_dict(), 201

@ns_country_city.route('/cities')
class CityList(Resource):
    @ns_country_city.doc('list_cities')
    @ns_country_city.marshal_list_with(city_model)
    def get(self):
        cities = City.load_all()
        return [city.to_dict() for city in cities]

@ns_country_city.route('/cities/<string:city_id>')
@ns_country_city.response(404, 'City not found')
@ns_country_city.param('city_id', 'The city identifier')
class CityResource(Resource):
    @ns_country_city.doc('get_city')
    @ns_country_city.marshal_with(city_model)
    def get(self, city_id):
        city = City.load(city_id)
        if not city:
            abort(404, description="City not found")
        return city.to_dict()

    @ns_country_city.doc('update_city')
    @ns_country_city.expect(city_model)
    @ns_country_city.marshal_with(city_model)
    def put(self, city_id):
        city = City.load(city_id)
        if not city:
            abort(404, description="City not found")

        if not request.json:
            abort(400, description="Request payload must be JSON")

        data = request.json
        validate_city_data(data)
        city.update_details(
            name=data['name'],
            country_id=data['country_id'] if 'country_id' in data else city.country_id
        )
        return city.to_dict()

    @ns_country_city.doc('delete_city')
    @ns_country_city.response(204, 'City deleted')
    def delete(self, city_id):
        city = City.load(city_id)
        if not city:
            abort(404, description="City not found")

        City.delete(city_id)
        return '', 204
