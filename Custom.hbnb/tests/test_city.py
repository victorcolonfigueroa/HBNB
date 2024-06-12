import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from models.city import City
from models.place import Place

class TestCity(unittest.TestCase):
    def test_create_city(self):
        city = City(name="Test City", country="Test Country")
        self.assertEqual(city.name, "Test City")
        self.assertEqual(city.country, "Test Country")

    def test_add_place(self):
        city = City(name="Test City", country="Test Country")
        place = Place(name="Test Place", description="Nice place", address="123 Main St", city=None, latitude=0.0, longitude=0.0, number_of_rooms=2, bathrooms=1, price_per_night=100, max_guests=4)
        city.add_place(place)
        self.assertIn(place, city.places)
        self.assertEqual(place.city, city)

if __name__ == '__main__':
    unittest.main()
