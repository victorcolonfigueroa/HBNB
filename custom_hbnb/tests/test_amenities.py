import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from model.amenitycls import Amenity

class TestAmenity(unittest.TestCase):
    def test_create_amenity(self):
        amenity = Amenity(name="Wi-Fi", description="Wireless internet")
        self.assertEqual(amenity.name, "Wi-Fi")
        self.assertEqual(amenity.description, "Wireless internet")

    def test_update_amenity(self):
        amenity = Amenity(name="Wi-Fi", description="Wireless internet")
        amenity.update_amenity(name="High-speed Wi-Fi")
        self.assertEqual(amenity.name, "High-speed Wi-Fi")

if __name__ == '__main__':
    unittest.main()
