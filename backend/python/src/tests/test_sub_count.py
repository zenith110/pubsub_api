import unittest
import os
from app import app
import json

# Tests the functionality of the subcount route
class Subcount(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass
    # Gets how many subs there currently are in the database
    def sub_count(self):
        response = self.app.get(
            "/subcount/",
        )

        # Checks to see that the number is a string
        self.assertIsInstance(response, str)
        

if __name__ == "__main__":
    unittest.main()