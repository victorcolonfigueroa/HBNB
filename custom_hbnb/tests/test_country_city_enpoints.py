import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json
from api import app

import unittest
import json
from api import app

class TestCountryCityEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_get_countries(self):
        response = self.client.get('/countries')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_country(self):
        # Pre-load a country
        country_data = {
            'name': 'United States',
            'code': 'US'
        }
        response = self.client.post('/countries', json=country_data)
        self.assertEqual(response.status_code, 201)  # Ensure the country is created

        response = self.client.get('/countries/US')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['code'], 'US')

    def test_get_country_cities(self):
        # Pre-load a country and a city
        country_data = {
            'name': 'United States',
            'code': 'US'
        }
        self.client.post('/countries', json=country_data)

        city_data = {
            'name': 'New York',
            'country_code': 'US'
        }
        response = self.client.post('/cities', json=city_data)
        self.assertEqual(response.status_code, 201)  # Ensure the city is created

        response = self.client.get('/countries/US/cities')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_create_city(self):
        # Create the country first
        country_code = 'US'
        country_data = {'code': country_code, 'name': 'United States'}
        response = self.client.post('/countries', json=country_data)
        self.assertEqual(response.status_code, 201)  # Ensure the country is created

        # Now create the city
        city_data = {'name': 'New York', 'country_code': country_code}
        response = self.client.post(f'/countries/{country_code}/cities/', json=city_data)
        self.assertEqual(response.status_code, 201)  # Ensure the city is created

    def test_create_city_invalid_country_code(self):
        response = self.app.post('/cities', json={
            'name': 'New York',
            'country_code': 'INVALID'
        })
        self.assertEqual(response.status_code, 400)

    def test_create_city_duplicate_name(self):
        # Pre-load a country
        country_data = {
            'name': 'United States',
            'code': 'US'
        }
        response = self.client.post('/countries', json=country_data)
        self.assertEqual(response.status_code, 201)  # Ensure the country is created

        # Create a city in the pre-loaded country
        city_data = {
            'name': 'New York',
            'country_code': 'US'
        }
        response = self.client.post('/countries/US/cities', json=city_data)
        self.assertEqual(response.status_code, 201)  # Ensure the city is created

        # Try to create a city with the same name in the same country
        response = self.client.post('/countries/US/cities', json=city_data)
        self.assertEqual(response.status_code, 409)  # Expect a conflict error

    def test_get_city(self):
        # Pre-load a country and a city
        country_data = {
            'name': 'United States',
            'code': 'US'
        }
        self.client.post('/countries', json=country_data)

        city_data = {
            'name': 'New York',
            'country_code': 'US'
        }
        create_response = self.client.post('/cities', json=city_data)
        city_id = json.loads(create_response.data)['id']

        response = self.client.get(f'/cities/{city_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'New York')

    def test_update_city(self):
        # Pre-load a country and a city
        country_data = {
            'name': 'United States',
            'code': 'US'
        }
        self.client.post('/countries', json=country_data)

        city_data = {
            'name': 'New York',
            'country_code': 'US'
        }
        create_response = self.client.post('/cities', json=city_data)
        city_id = json.loads(create_response.data)['id']

        response = self.client.put(f'/cities/{city_id}', json={
            'name': 'Updated City'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Updated City')

    def test_delete_city(self):
        # Pre-load a country and a city
        country_data = {
            'name': 'United States',
            'code': 'US'
        }
        self.app.post('/countries', json=country_data)

        city_data = {
            'name': 'New York',
            'country_code': 'US'
        }
        create_response = self.client.post('/cities', json=city_data)
        print(create_response.data)

        # Check the status code and data of create_response
        if create_response.status_code == 200 and create_response.data:
            city_id = json.loads(create_response.data)['id']
        else:
            self.fail(f"Failed to create city: {create_response.data}")

        response = self.client.delete(f'/cities/{city_id}')
        self.assertEqual(response.status_code, 204)

    def test_get_nonexistent_city(self):
        response = self.client.get('/cities/nonexistent_id')
        self.assertEqual(response.status_code, 404)

    def test_update_nonexistent_city(self):
        response = self.client.put('/cities/nonexistent_id', json={
            'name': 'Updated City'
        })
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_city(self):
        response = self.client.delete('/cities/nonexistent_id')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
