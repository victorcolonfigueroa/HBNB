from flask import request, jsonify, abort
from flask_restx import Resource, fields
from api import api
from models.country import Country
from models.city import City
from werkzeug.exceptions import HTTPException
from persistence.data_manager import DataManager
from persistence.file_storage import FileStorage

# Create an instance of DataManager
storage = FileStorage()
data_manager = DataManager(storage) 

# Define a namespace for countries and cities
ns_country = api.namespace('countries', description='Country operations')
ns_city = api.namespace('cities', description='City operations')

# Define models for countries and cities
country_model = api.model('Country', {
    'id': fields.String(readOnly=True, description='The unique identifier of a country'),
    'name': fields.String(required=True, description='The country name'),
    'code': fields.String(required=True, description='The country ISO code'),
    'created_at': fields.DateTime(readOnly=True, description='The date and time the country was created'),
    'updated_at': fields.DateTime(readOnly=True, description='The date and time the country was last updated')
})

city_model = api.model('City', {
    'id': fields.String(readOnly=True, description='The unique identifier of a city'),
    'name': fields.String(required=True, description='The city name'),
    'country_code': fields.String(required=True, description='The ISO code of the country'),
    'created_at': fields.DateTime(readOnly=True, description='The date and time the city was created'),
    'updated_at': fields.DateTime(readOnly=True, description='The date and time the city was last updated')
})

def validate_city_data(data):
    """
    Validates city data. Checks if the name and country code are present and valid.
    
    Args:
        data (dict): The city data to validate.
        
    Raises:
        HTTPException: If the name or country code are not valid, or the country code does not exist.
    """
    if 'name' not in data or not isinstance(data['name'], str) or not data['name'].strip():
        abort(400, description="City name must be a non-empty string")
    if 'country_code' not in data or not isinstance(data['country_code'], str) or not data['country_code'].strip():
        abort(400, description="Country code must be a non-empty string")
    country = Country.load_by_code(data['country_code'])
    if not country:
        abort(400, description="Invalid country code")

@ns_country.route('/')
class CountryList(Resource):
    """
    Resource for handling the HTTP methods for the /countries route.
    """
    @ns_country.doc('list_countries')
    @ns_country.marshal_list_with(country_model)
    def get(self):
        """
        Returns a list of all countries.
        
        Returns:
            A list of countries.
        """
        countries = Country.load_all()
        return countries
    
    @ns_country.doc('create_country')
    @ns_country.expect(country_model)
    @ns_country.marshal_with(country_model, code=201)
    def post(self):
        """
        Creates a new country with the data provided in the request.
        Returns:
            The created country, with a status code of 201.
            
        Raises:
            HTTPException: If the request payload is not JSON, or the country data is not valid.
        """
        if not request.json:
            abort(400, description="Request payload must be JSON")
        data = request.json
        if 'name' not in data or not isinstance(data['name'], str) or not data['name'].strip():
            abort(400, description="Country name must be a non-empty string")
        if 'code' not in data or not isinstance(data['code'], str) or not data['code'].strip():
            abort(400, description="Country code must be a non-empty string")
        try:
            country = Country(name=data['name'], code=data['code'])
            data_manager.save(country)  # Assuming you have a save method to persist the country
            return country, 201
        except ValueError as e:
            abort(400, description=str(e))

@ns_country.route('/<string:country_code>')
@ns_country.response(404, 'Country not found')
@ns_country.param('country_code', 'The country ISO code')
class CountryResource(Resource):
    """
    Resource for handling the HTTP methods for the /countries/<country_code> route.
    """
    @ns_country.doc('get_country')
    @ns_country.marshal_with(country_model)
    def get(self, country_code):
        """
        Returns the country with the given ISO code.
        
        Args:
            country_code (str): The ISO code of the country to return.
            
        Returns:
            The country with the given ISO code.
            
        Raises:
            HTTPException: If the country is not found.
        """
        country = Country.load_by_code(country_code)
        if not country:
            abort(404, description="Country not found")
        return country

@ns_country.route('/<string:country_code>/cities')
@ns_country.response(404, 'Country not found')
@ns_country.param('country_code', 'The country ISO code')
class CountryCities(Resource):
    """
    Resource for handling the HTTP methods for the /countries/<country_code>/cities route.
    """
    @ns_country.doc('list_country_cities')
    @ns_country.marshal_list_with(city_model)
    def get(self, country_code):
        """
        Returns a list of all cities in the country with the given ISO code.
        
        Args:
            country_code (str): The ISO code of the country to return the cities for.
            
        Returns:
            A list of cities in the country with the given ISO code.
            
        Raises:
            HTTPException: If the country is not found.
        """
        country = Country.load_by_code(country_code)
        if not country:
            abort(404, description="Country not found")
        cities = [city for city in City.load_all() if city.country_code == country_code]
        return cities

@ns_city.route('/')
class CityList(Resource):
    """
    Resource for handling the HTTP methods for the /cities route.
    """
    @ns_city.doc('list_cities')
    @ns_city.marshal_list_with(city_model)
    def get(self):
        """
        Returns a list of all cities.
        
        Returns:
            A list of cities.
        """
        cities = City.load_all()
        return cities

    @ns_city.doc('create_city')
    @ns_city.expect(city_model)
    @ns_city.marshal_with(city_model, code=201)
    def post(self):
        """
        Creates a new city with the data provided in the request.
        
        Returns:
            The created city, with a status code of 201.
            
        Raises:
            HTTPException: If the request payload is not JSON, the city data is not valid, or the city name already exists in the country.
        """
        if not request.json:
            abort(400, description="Request payload must be JSON")
        data = request.json
        validate_city_data(data)

        name = data['name']
        country_code = data['country_code']

        for city in City.load_all():
            if city.name == name and city.country_code == country_code:
                abort(409, description="City name already exists in this country")

        try:
            country = Country.load_by_code(country_code)
            city = City(name=name, country_code=country.code)
            data_manager.save(city)
            return city, 201
        except ValueError as e:
            abort(400, description=str(e))

@ns_city.route('/<string:city_id>')
@ns_city.response(404, 'City not found')
@ns_city.param('city_id', 'The city identifier')
class CityResource(Resource):
    """
    Resource for handling the HTTP methods for the /cities/<city_id> route.
    """
    @ns_city.doc('get_city')
    @ns_city.marshal_with(city_model)
    def get(self, city_id):
        """
        Returns the city with the given ID.
        
        Args:
            city_id (str): The ID of the city to return.
            
        Returns:
            The city with the given ID.
            
        Raises:
            HTTPException: If the city is not found.
        """
        city = City.load(city_id)
        if not city:
            abort(404, description="City not found")
        return city

    @ns_city.doc('update_city')
    @ns_city.expect(city_model)
    @ns_city.marshal_with(city_model)
    def put(self, city_id):
        """
        Updates the city with the given ID with the data provided in the request.
        
        Args:
            city_id (str): The ID of the city to update.
            
        Returns:
            The updated city.
            
        Raises:
            HTTPException: If the city is not found, the request payload is not JSON, the city data is not valid, or the city name already exists in the country.
        """
        city = City.load(city_id)
        if not city:
            abort(404, description="City not found")

        if not request.json:
            abort(400, description="Request payload must be JSON")

        data = request.json
        validate_city_data(data)

        name = data.get('name')
        country_code = data.get('country_code')

        if (name and name != city.name) or (country_code and country_code != city.country_code):
            for c in City.load_all():
                if c.name == name and c.country_code == country_code:
                    abort(409, description="City name already exists in this country")

        try:
            country = Country.load_by_code(country_code)
            city.update_details(name=name, country_code=country.code)
            data_manager.save(city)
            return city
        except ValueError as e:
            abort(400, description=str(e))

    @ns_city.doc('delete_city')
    @ns_city.response(204, 'City deleted')
    def delete(self, city_id):
        """
        Deletes the city with the given ID.
        
        Args:
            city_id (str): The ID of the city to delete.
            
        Returns:
            An empty response with a status code of 204.
            
        Raises:
            HTTPException: If the city is not found.
        """
        try:
            city = City.load(city_id)
            if city is None:
                abort(404, description="City not found")
            city.delete(city_id)
            return '', 204
        except Exception as e:
            abort(500, description=str(e))
