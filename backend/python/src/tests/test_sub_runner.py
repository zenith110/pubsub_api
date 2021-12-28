import unittest
import os
from app import app
import json

# Tests the functionality of 
class SubRunner(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass
    # Given a chicken tenders input, check to see that the types are all strings
    def chicken_tenders_get(self):
        response = self.app.get(
            "/subs/?name=chicken-tenders",
        )
        
        # Verify that all the types are correct
        # Data changes frequently, however types does not
        response_data = response.get_json()
        self.assertIsInstance(response_data[0]["sub_name"], str)
        self.assertIsInstance(response_data[0]["last_sale"], str)
        self.assertIsInstance(response_data[0]["status"], str)
        self.assertIsInstance(response_data[0]["price"], str)
        self.assertIsInstance(response_data[0]["image"], str)

if __name__ == "__main__":
    unittest.main()