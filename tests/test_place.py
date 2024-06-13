import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.review import Review

class TestPlace(unittest.TestCase):
    def test_create_place(self):
        city = City(name="Test City", country="Test Country")
        place = Place(name="Test Place", description="Nice place", address="123 Main St", city=city, latitude=0.0, longitude=0.0, number_of_rooms=2, bathrooms=1, price_per_night=100, max_guests=4)
        self.assertEqual(place.name, "Test Place")
        self.assertEqual(place.city, city)
    
    def test_update_details(self):
        city = City(name="Test City", country="Test Country")
        place = Place(name="Test Place", description="Nice place", address="123 Main St", city=city, latitude=0.0, longitude=0.0, number_of_rooms=2, bathrooms=1, price_per_night=100, max_guests=4)
        place.update_details(name="New Place", price_per_night=150)
        self.assertEqual(place.name, "New Place")
        self.assertEqual(place.price_per_night, 150)

    def test_add_amenity(self):
        place = Place(name="Test Place", description="Nice place", address="123 Main St", city=None, latitude=0.0, longitude=0.0, number_of_rooms=2, bathrooms=1, price_per_night=100, max_guests=4)
        amenity = Amenity(name="Wi-Fi", description="Wireless internet")
        place.add_amenity(amenity)
        self.assertIn(amenity, place.amenities)

    def test_add_review(self):
        city = City(name="Test City", country="Test Country")
        place = Place(name="Test Place", description="Nice place", address="123 Main St", city=city, latitude=0.0, longitude=0.0, number_of_rooms=2, bathrooms=1, price_per_night=100, max_guests=4)
        user = User(email="test@example.com", password="password", first_name="Test", last_name="User")
        review = Review(user=user, place=place, rating=5, comment="Great place!")
        place.add_review(review)
        self.assertIn(review, place.reviews)

if __name__ == '__main__':
    unittest.main()
