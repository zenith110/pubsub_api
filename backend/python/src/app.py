from flask import Flask, render_template, request, jsonify, Config
import requests
import json
from flask_cors import CORS, cross_origin
from services import newsletter
from services import sub_runner
from services import on_sale_service
from services import sub_count
from services import random_subs
from services import all_subs
from flasgger import Swagger, swag_from
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
app = Flask(__name__, static_url_path="/static")
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
swagger = Swagger(app)
limiter = Limiter(
    app, key_func=get_remote_address, default_limits=["200 per day, 50 per hour"]
)
class NewsLetter:
    def __init__(self, api_key, domain, sender, overall) :
        self.api_key = api_key
        self.domain = domain
        self.sender = sender
        self.overall = overall
class DatabaseObject:
    def __init__(self) -> None:
        self.user = ""
        self.password = ""
        self.host = ""
        self.port = ""
        self.database = ""
        self.table = ""

db = DatabaseObject()
db.user = os.getenv("USERNAME_DB")
db.password = os.getenv("PASSWORD")
db.host = os.getenv("DBHOST")
db.port = os.getenv("PORT")
db.database = os.getenv("DATABASE")
db.table = os.getenv("TABLE")

"""
Gets the current sub count
"""


@app.route("/totalcount/", methods=["GET"])
def num():
    """Fetches the total amount of subs that we have available
    ---
    responses:
        200:
            description: How many subs we have

    """
    sub_count_data = sub_count.count()
    return sub_count_data


"""
Adds a email and first name to the pubsub sales newsletter
"""


@app.route("/email/", methods=["POST"])
def email():
    content = request.json
    """
    Parses the JSON data to be dumped into a mailchimp list
    """
    email = content["email"]
    first_name = content["name"]
    checked_subs = content["checkedSubs"]
    """
    Sends off data to add to list
    """
    sender = os.getenv("SENDER")
    domain = os.getenv("DOMAIN")
    api_key = os.getenv("API_KEY")
    overall = os.getenv("OVERALL_MAILING_LIST")
    email_object = NewsLetter(api_key, domain, sender, overall)
    email = newsletter.register_data(email, first_name, checked_subs, email_object)
    return email


"""
Returns all the sub data for the frontend
"""


@app.route("/onsale/", methods=["GET"])
def onsale_data():
    """Gets all the pubsubs data including name, price, image and other various data.
    ---
    responses:
        200:
            description: Subs data in json.
        404:
            description: Subs could not be found, an error occured.

    """
    on_sale_post = on_sale_service.on_sale_check(db)
    return on_sale_post


"""
Returns all the sub names
"""


@app.route("/allsubs/", methods=["GET"])
def all_names():
    """Fetches all the pubsubs we have available
    ---
    responses:
        200:
            description: Sub's names in JSON
    """
    return all_subs.all_subs_data(db)
"""
Fetches a sub based on the sub name provided
"""
@app.route("/subs/", methods=["GET"])
def sub():
    """Fetches pubsub
    Name requires hyphens when using a sub with spaces
    If random is provided as a name, will return a random sub
    ---
    parameters:
      - name: name
        in: query
        type: string
        required: true
    responses:
        200:
            description: Sub JSON response
        400:
            description: Sub could not be found

    """
    if request.method == "GET":
        sub_name = request.args.get("name")
        if sub_name == "random":
            sub = random_sub(db)
            return sub
        else:
            sub = sub_runner.sub_runner_checker(sub_name, db)
            return sub


"""
Generates a random sub from the database
"""


def random_sub(db):
    random_sub = random_subs.random_subs(db)
    return random_sub


"""
Uses a sub name to fetch the data on it
"""


def sub_runner_path(sub_name):
    sub = sub_runner.sub_runner_checker(sub_name, db)
    return sub


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
