import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from models.user import User
from models.place import Place


class TestUser(unittest.TestCase):
    def setUp(self):
        User.users = {}

    def test_create_user(self):
        user = User(email="test@example.com", password="password", first_name="Test", last_name="User")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")

    def test_update_profile(self):
        user = User(email="test@example.com", password="password", first_name="Test", last_name="User")
        user.update_profile(email="new@example.com", first_name="New")
        self.assertEqual(user.email, "new@example.com")
        self.assertEqual(user.first_name, "New")

    def test_unique_email(self):
        user1 = User(email="test@example.com", password="password", first_name="Test", last_name="User")
        with self.assertRaises(ValueError):
            User(email="test@example.com", password="password", first_name="Test", last_name="User")

    def test_host_place(self):
        user = User(email="test@example.com", password="password", first_name="Test", last_name="User")
        place = Place(name="Test Place", description="Nice place", address="123 Main St", city="Test City", latitude=0.0, longitude=0.0, number_of_rooms=2, bathrooms=1, price_per_night=100, max_guests=4)
        user.host_place(place)
        self.assertEqual(place.host, user)

    def test_host_place_already_hosted(self):
        user1 = User(email="host1@example.com", password="password", first_name="Host", last_name="One")
        user2 = User(email="host2@example.com", password="password", first_name="Host", last_name="Two")
        place = Place(name="Test Place", description="Nice place", address="123 Main St", city="Test City", latitude=0.0, longitude=0.0, number_of_rooms=2, bathrooms=1, price_per_night=100, max_guests=4)
        user1.host_place(place)
        with self.assertRaises(ValueError):
            user2.host_place(place)

if __name__ == '__main__':
    unittest.main()
