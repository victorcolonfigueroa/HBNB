import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.city import City
from models.country import Country
from persistence.file_storage import FileStorage
from persistence.data_manager import DataManager


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.storage = FileStorage('test_file_storage.json')
        self.data_manager = DataManager(self.storage)
        User.users.clear()

    def tearDown(self):
        if os.path.exists('test_file_storage.json'):
            os.remove('test_file_storage.json')

    def test_save_and_load_user(self):
        user = User(email="test@example.com", password="password", first_name="Test", last_name="User")
        self.data_manager.save(user)
        loaded_user = self.data_manager.load(User, user.id)
        self.assertEqual(user.email, loaded_user.email) \

    def test_delete_user(self):
        user = User(email="test@example.com", password="password", first_name="Test", last_name="User")
        self.data_manager.save(user)
        self.data_manager.delete(user)
        loaded_user = self.data_manager.load(User, user.id)
        self.assertIsNone(loaded_user)

    def test_save_and_load_place(self):
        city = City(name="Test City", country="Test Country")
        place = Place(name="Test Place", description="Nice place", address="123 Main St", city=city, latitude=0.0, longitude=0.0, number_of_rooms=2, bathrooms=1, price_per_night=100, max_guests=4)
        self.data_manager.save(place)
        loaded_place = self.data_manager.load(Place, place.id)
        self.assertEqual(place.name, loaded_place.name)

    def test_save_and_load_city(self):
        city = City(name="Test City", country="Test Country")
        self.data_manager.save(city)
        loaded_city = self.data_manager.load(City, city.id)
        self.assertEqual(city.name, loaded_city.name)

    def test_save_and_load_review(self):
        user = User(email="test@example.com", password="test", first_name="Test", last_name="User")
        self.data_manager.save(user)
        city = City(name="Test City", country="Test Country")
        self.data_manager.save(city)
        place = Place(name="Test Place", description="Nice place", address="123 Main St", city=city, latitude=0.0, longitude=0.0, number_of_rooms=2, bathrooms=1, price_per_night=100, max_guests=4)
        self.data_manager.save(place)
        review = Review(user=user, place=place, comment="This is a test review", rating=5)
        self.data_manager.save(review)
        loaded_review = self.data_manager.load(Review, review.id)
        self.assertEqual(review.comment, loaded_review.comment)
        self.assertEqual(review.rating, loaded_review.rating)

    def test_save_and_load_amenity(self):
        amenity = Amenity(name="Test Amenity", description="This is a test amenity")
        self.data_manager.save(amenity)
        loaded_amenity = self.data_manager.load(Amenity, amenity.id)
        self.assertEqual(amenity.name, loaded_amenity.name)
        self.assertEqual(amenity.description, loaded_amenity.description)

    def test_save_and_load_country(self):
        country = Country(name="Test Country")
        self.data_manager.save(country)
        loaded_country = self.data_manager.load(Country, country.id)
        self.assertEqual(country.name, loaded_country.name)


if __name__ == '__main__':
    unittest.main()
