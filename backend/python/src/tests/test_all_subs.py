import unittest
import os
from app import app
import json

# Tests the functionality of the allsubs route
class AllSubs(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass
    # Given a random sub input, check to see that the types are all strings
    def all_subs(self):
        response = self.app.get(
            "/allsubs/",
        )
        
        # Verify that all the types are correct
        # Data changes frequently, however types does not
        response_data = response.get_json()
        for index in range(0, len(response_data)):
            self.assertIsInstance(response_data[index]["sub_name"], str)
            self.assertIsInstance(response_data[index]["last_sale"], str)
            self.assertIsInstance(response_data[index]["status"], str)
            self.assertIsInstance(response_data[index]["price"], str)
            self.assertIsInstance(response_data[index]["image"], str)

if __name__ == "__main__":
    unittest.main()