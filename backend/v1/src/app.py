from flask import Flask, render_template, request
import requests
import json
from flask_cors import CORS
from services import mailchimp
from services import sub_runner
from services import on_sale_service
from services import sub_count
from services import phone_adding
from services import all_subs
from services import random_subs

app = Flask(__name__, static_url_path="/static")
CORS(app)
"""
Route to add phone numbers
"""


@app.route("/phone/", methods=["POST", "GET"])
def phone_add():
    content = request.json
    phone_number = content["phoneNumber"]
    phone_adding.add_phone(phone_number)


"""
Gets the current sub count
"""


@app.route("/totalcount/", methods=["POST", "GET"])
def num():
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
    email = mailchimp.register_data(email, first_name, checked_subs)
    return email


"""
Returns all the sub data for the frontend
"""


@app.route("/onsale/", methods=["POST", "GET"])
def onsale_data():
    on_sale_post = on_sale_service.on_sale_check()
    return on_sale_post


"""
Returns all the sub names
"""


@app.route("/allsubs/", methods=["POST", "GET"])
def all_names():
    all_subs.all_subs_data()


"""
Fetches a sub based on the sub name provided
"""


@app.route("/subs/", methods=["POST", "GET"])
def sub():
    if request.method == "GET":
        sub_name = request.args.get("name")
        if sub_name == "":
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
    print("Off to the function it goes!")
    sub = sub_runner.sub_runner_checker(sub_name)
    return sub





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
