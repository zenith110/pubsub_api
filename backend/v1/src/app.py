from flask import Flask, render_template, request, jsonify, Config
import requests
import json
from flask_cors import CORS
from services import newsletter
from services import sub_runner
from services import on_sale_service
from services import sub_count
from services import all_subs
from services import random_subs
from flasgger import Swagger, swag_from
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__, static_url_path="/static")
CORS(app)

swagger = Swagger(app)
limiter = Limiter(
    app, key_func=get_remote_address, default_limits=["200 per day, 50 per hour"]
)
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
    email = newsletter.register_data(email, first_name, checked_subs)
    return email


"""
Returns all the sub data for the frontend
"""


@app.route("/onsale/", methods=["GET"])
def onsale_data():
    """Gets all the pubsubs data
    ---
    responses:
        200:
            description: Sub's names in JSON

    """
    on_sale_post = on_sale_service.on_sale_check()
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
    return all_subs.all_subs_data()


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
            sub = random_sub()
            return sub
        else:
            sub = sub_runner_path(sub_name)
            return sub


"""
Generates a random sub from the database
"""


def random_sub():
    random_sub = random_subs.random_subs()
    return random_sub


"""
Uses a sub name to fetch the data on it
"""


def sub_runner_path(sub_name):
    sub = sub_runner.sub_runner_checker(sub_name)
    return sub


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
