from flask import request, jsonify, abort
from flask_restx import Resource, fields
from api import api
from models.country import Country
from models.city import City

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
    @ns_country.doc('list_countries') # Document the list_countries method
    @ns_country.marshal_list_with(country_model) # Use the country_model to serialize the response
    def get(self):
        """
        Returns a list of all countries.
        
        Returns:
            A list of countries.
        """
        countries = Country.load_all() # Load all countries from the database
        return countries

@ns_country.route('/<string:country_code>') # Define the route /countries/<country_code>
@ns_country.response(404, 'Country not found') # Add a 404 response description
@ns_country.param('country_code', 'The country ISO code') # Add a parameter description
class Country(Resource):
    """
    Resource for handling the HTTP methods for the /countries/<country_code> route.
    """
    @ns_country.doc('get_country') # Document the get_country method
    @ns_country.marshal_with(country_model) # Use the country_model to serialize the response
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
        country = Country.load_by_code(country_code) # Load the country with the given ISO code
        if not country:
            abort(404, description="Country not found") # Return a 404 response if the country is not found
        return country

@ns_country.route('/<string:country_code>/cities') # Define the route /countries/<country_code>/cities
@ns_country.response(404, 'Country not found')
@ns_country.param('country_code', 'The country ISO code')
class CountryCities(Resource):
    """
    Resource for handling the HTTP methods for the /countries/<country_code>/cities route.
    """
    @ns_country.doc('list_country_cities') # Document the list_country_cities method
    @ns_country.marshal_list_with(city_model) # Use the city_model to serialize the response
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
        country = Country.load_by_code(country_code) # Load the country with the given ISO code
        if not country:
            abort(404, description="Country not found")
        # Filter cities by country code    
        cities = [city for city in City.load_all() if city.country.code == country_code]
        return cities

@ns_city.route('/') # Define the route /cities
class CityList(Resource):
    """
    Resource for handling the HTTP methods for the /cities route.
    """
    @ns_city.doc('list_cities') # Document the list_cities method
    @ns_city.marshal_list_with(city_model) # Use the city_model to serialize the response
    def get(self):
        """
        Returns a list of all cities.
        
        Returns:
            A list of cities.
        """
        cities = City.load_all() # Load all cities from the database
        return cities

    @ns_city.doc('create_city') # Document the create_city method
    @ns_city.expect(city_model) # Expect a city_model in the request payload
    @ns_city.marshal_with(city_model, code=201) # Use the city_model to serialize the response with a status code of 201
    def post(self):
        """
        Creates a new city with the data provided in the request.
        
        Returns:
            The created city, with a status code of 201.
            
        Raises:
            HTTPException: If the request payload is not JSON, the city data is not valid, or the city name already exists in the country.
        """
        if not request.json:
            # Return a 400 Bad Request response if the request payload is not JSON
            abort(400, description="Request payload must be JSON")
        data = request.json # Get the JSON data from the request
        validate_city_data(data) # Validate the city data

        name = data['name'] # Get the city name from the data
        country_code = data['country_code'] # Get the country code from the data

        for city in City.load_all(): # Check if the city name already exists in the country
            # If the city name and country code already exist, return a 409 Conflict response
            if city.name == name and city.country.code == country_code:
                abort(409, description="City name already exists in this country")

        try:
            country = Country.load_by_code(country_code) # Load the country with the given ISO code
            city = City(name=name, country=country) # Create a new city with the provided data
            return city, 201 # Return the city with a status code of 201
        except ValueError as e:
            abort(400, description=str(e))

@ns_city.route('/<string:city_id>') # Define the route /cities/<city_id>
@ns_city.response(404, 'City not found') # Add a 404 response description
@ns_city.param('city_id', 'The city identifier') # Add a parameter description
class City(Resource):
    """
    Resource for handling the HTTP methods for the /cities/<city_id> route.
    """
    @ns_city.doc('get_city') # Document the get_city method
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
        city = City.load(city_id) # Load the city with the given ID
        if not city:
            abort(404, description="City not found")
        return city

    @ns_city.doc('update_city') # Document the update_city method
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

        name = data.get('name') # Get the city name from the data
        country_code = data.get('country_code') # Get the country code from the data

        # Check if the city name already exists in the country
        if (name and name != city.name) or (country_code and country_code != city.country.code):
            for c in City.load_all():
                if c.name == name and c.country.code == country_code:
                    abort(409, description="City name already exists in this country")

        try:
            # Update the city details
            country = Country.load_by_code(country_code)
            city.update_details(name=name, country=country) # Update the city with the provided data
            return city
        except ValueError as e:
            abort(400, description=str(e))

    @ns_city.doc('delete_city') # Document the delete_city method
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
        city = City.load(city_id)
        if not city:
            abort(404, description="City not found")

        City.delete(city_id) # Delete the city
        return '', 204 # Return an empty response with a status code of 204
