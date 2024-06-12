import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from models.country import Country
from models.city import City

class TestCountry(unittest.TestCase):
    def test_create_country(self):
        country = Country(name="Test Country")
        self.assertEqual(country.name, "Test Country")

    def test_add_city(self):
        country = Country(name="Test Country")
        city = City(name="Test City", country=country)
        country.add_city(city)
        self.assertIn(city, country.cities)

if __name__ == '__main__':
    unittest.main()
