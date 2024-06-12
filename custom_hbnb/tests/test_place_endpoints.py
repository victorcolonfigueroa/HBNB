import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json
from app import app

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_place(self):
        # Pre-load a city, user, and amenities
        city_response = self.app.post('/cities', json={
            'name': 'New York',
            'country_code': 'US'
        })
        city_id = json.loads(city_response.data)['id']

        user_response = self.app.post('/users', json={
            'email': 'host@example.com',
            'password': 'password',
            'first_name': 'Host',
            'last_name': 'User'
        })
        host_id = json.loads(user_response.data)['id']

        amenity_response = self.app.post('/amenities', json={
            'name': 'WiFi'
        })
        amenity_id = json.loads(amenity_response.data)['id']

        response = self.app.post('/places', json={
            'name': 'Beautiful Apartment',
            'description': 'A beautiful apartment in New York',
            'address': '123 Main St',
            'city_id': city_id,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'host_id': host_id,
            'number_of_rooms': 3,
            'number_of_bathrooms': 2,
            'price_per_night': 150.00,
            'max_guests': 4,
            'amenity_ids': [amenity_id]
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Beautiful Apartment')
        self.assertEqual(data['city_id'], city_id)
        self.assertEqual(data['host_id'], host_id)
        self.assertEqual(data['amenity_ids'], [amenity_id])

    def test_get_places(self):
        response = self.app.get('/places')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_place(self):
        # Pre-load a place
        city_response = self.app.post('/cities', json={
            'name': 'New York',
            'country_code': 'US'
        })
        city_id = json.loads(city_response.data)['id']

        user_response = self.app.post('/users', json={
            'email': 'host@example.com',
            'password': 'password',
            'first_name': 'Host',
            'last_name': 'User'
        })
        host_id = json.loads(user_response.data)['id']

        amenity_response = self.app.post('/amenities', json={
            'name': 'WiFi'
        })
        amenity_id = json.loads(amenity_response.data)['id']

        create_response = self.app.post('/places', json={
            'name': 'Beautiful Apartment',
            'description': 'A beautiful apartment in New York',
            'address': '123 Main St',
            'city_id': city_id,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'host_id': host_id,
            'number_of_rooms': 3,
            'number_of_bathrooms': 2,
            'price_per_night': 150.00,
            'max_guests': 4,
            'amenity_ids': [amenity_id]
        })
        place_id = json.loads(create_response.data)['id']

        response = self.app.get(f'/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Beautiful Apartment')
        self.assertEqual(data['city_id'], city_id)
        self.assertEqual(data['host_id'], host_id)
        self.assertEqual(data['amenity_ids'], [amenity_id])

    def test_update_place(self):
        # Pre-load a place
        city_response = self.app.post('/cities', json={
            'name': 'New York',
            'country_code': 'US'
        })
        city_id = json.loads(city_response.data)['id']

        user_response = self.app.post('/users', json={
            'email': 'host@example.com',
            'password': 'password',
            'first_name': 'Host',
            'last_name': 'User'
        })
        host_id = json.loads(user_response.data)['id']

        amenity_response = self.app.post('/amenities', json={
            'name': 'WiFi'
        })
        amenity_id = json.loads(amenity_response.data)['id']

        create_response = self.app.post('/places', json={
            'name': 'Beautiful Apartment',
            'description': 'A beautiful apartment in New York',
            'address': '123 Main St',
            'city_id': city_id,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'host_id': host_id,
            'number_of_rooms': 3,
            'number_of_bathrooms': 2,
            'price_per_night': 150.00,
            'max_guests': 4,
            'amenity_ids': [amenity_id]
        })
        place_id = json.loads(create_response.data)['id']

        response = self.app.put(f'/places/{place_id}', json={
            'name': 'Updated Apartment',
            'description': 'An updated apartment in New York',
            'address': '123 Main St',
            'city_id': city_id,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'host_id': host_id,
            'number_of_rooms': 3,
            'number_of_bathrooms': 2,
            'price_per_night': 150.00,
            'max_guests': 4,
            'amenity_ids': [amenity_id]
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Updated Apartment')
        self.assertEqual(data['city_id'], city_id)
        self.assertEqual(data['host_id'], host_id)
        self.assertEqual(data['amenity_ids'], [amenity_id])

    def test_delete_place(self):
        # Pre-load a place
        city_response = self.app.post('/cities', json={
            'name': 'New York',
            'country_code': 'US'
        })
        city_id = json.loads(city_response.data)['id']

        user_response = self.app.post('/users', json={
            'email': 'host@example.com',
            'password': 'password',
            'first_name': 'Host',
            'last_name': 'User'
        })
        host_id = json.loads(user_response.data)['id']

        amenity_response = self.app.post('/amenities', json={
            'name': 'WiFi'
        })
        amenity_id = json.loads(amenity_response.data)['id']

        create_response = self.app.post('/places', json={
            'name': 'Beautiful Apartment',
            'description': 'A beautiful apartment in New York',
            'address': '123 Main St',
            'city_id': city_id,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'host_id': host_id,
            'number_of_rooms': 3,
            'number_of_bathrooms': 2,
            'price_per_night': 150.00,
            'max_guests': 4,
            'amenity_ids': [amenity_id]
        })
        place_id = json.loads(create_response.data)['id']

        response = self.app.delete(f'/places/{place_id}')
        self.assertEqual(response.status_code, 204)

    def test_get_nonexistent_place(self):
        response = self.app.get('/places/nonexistent_id')
        self.assertEqual(response.status_code, 404)

    def test_update_nonexistent_place(self):
        response = self.app.put('/places/nonexistent_id', json={
            'name': 'Updated Apartment'
        })
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_place(self):
        response = self.app.delete('/places/nonexistent_id')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
