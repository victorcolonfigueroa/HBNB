import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import unittest
from models.review import Review
from models.user import User
from models.place import Place
from models.city import City

class TestReview(unittest.TestCase):
    def setUp(self):
        User.users = {}

    def test_create_review(self):
        user = User(email="test@example.com", password="password", first_name="Test", last_name="User")
        city = City(name="Test City", country="Test Country")
        place = Place(name="Test Place", description="Nice place", address="123 Main St", city=city, latitude=0.0, longitude=0.0, number_of_rooms=2, bathrooms=1, price_per_night=100, max_guests=4)
        review = Review(user=user, place=place, rating=5, comment="Great place!")
        self.assertEqual(review.user, user)
        self.assertEqual(review.place, place)
        self.assertEqual(review.rating, 5)
    
    def test_update_review(self):
        user = User(email="test@example.com", password="password", first_name="Test", last_name="User")
        city = City(name="Test City", country="Test Country")
        place = Place(name="Test Place", description="Nice place", address="123 Main St", city=city, latitude=0.0, longitude=0.0, number_of_rooms=2, bathrooms=1, price_per_night=100, max_guests=4)
        review = Review(user=user, place=place, rating=5, comment="Great place!")
        review.update_review(rating=4, comment="Good place!")
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, "Good place!")

if __name__ == '__main__':
    unittest.main()
