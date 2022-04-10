import requests
import re
import os
from discord_webhook import DiscordWebhook, DiscordEmbed
import db_utils
import mailgun
import datetime
from itertools import chain
import boto3
import s3_utils
from dotenv import load_dotenv
from os.path import join, dirname


class Pubsub:
    def __init__(self) -> None:
        self.pubsub_name = []
        self.date = []
        self.price = []
        self.image_original = []
        self.image = []


class DatabaseObject:
    def __init__(self) -> None:
        self.user = ""
        self.password = ""
        self.host = ""
        self.port = ""
        self.database = ""
        self.table = ""


class MailgunObject:
    def __init__(self) -> None:
        self.sender_email = ""
        self.domain = ""
        self.mail_api_key = ""


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

s3 = boto3.resource(
    service_name="s3",
    region_name="us-east-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

my_bucket = s3.Bucket(os.getenv("BUCKET_NAME"))

db_object = DatabaseObject()
db_object.user = os.getenv("USERNAME_DB")
db_object.password = os.getenv("PASSWORD")
db_object.host = os.getenv("HOST")
db_object.port = os.getenv("PORT")
db_object.database = os.getenv("DATABASE")
db_object.table = os.getenv("TABLE")

mailgun_instance = MailgunObject()
mailgun_instance.sender_email = os.getenv("SENDER")
mailgun_instance.domain = os.getenv("DOMAIN")
mailgun_instance.mail_api_key = os.getenv("MAILGUN_API_KEY")
# the new implementation using Requests

# Given a month full name, convert to a singular number


def convert_month_to_numerical(month: str):
    month_to_num = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }
    for month_name, month_number_representation in month_to_num.items():
        if month in month_name:
            return month_number_representation


def scrape_publix_job():
    sub_sale_list = parse_publix_deli_page(os.getenv("ZIPCODE"))
    connection = db_utils.connect(db_object)
    cur = connection.cursor()
    """
    Set all the subs to false
    """
    on_sale = "False"
    make_all_subs_false = "Update {table} SET on_sale ='{on_sale}'"
    update_query = cur.execute(
        make_all_subs_false.format(
            table=db_utils.get_table(db_object),
            on_sale=on_sale,
        )
    )
    for i in range(0, len(sub_sale_list.pubsub_name)):
        db_utils.sub_check(
            sub_sale_list.pubsub_name[i],
            sub_sale_list.date[i],
            sub_sale_list.price[i],
            sub_sale_list.image[i],
            cur,
            db_object,
            os.getenv("WEBHOOK"),
            mailgun_instance,
        )
    db_utils.close(connection)


def find_closest_publix(zipCode):
    # Make a request to the publix servics endpoint to get the closest location
    response = requests.request(
        "GET",
        "https://services.publix.com/api/v1/storelocation",
        data="",
        headers={},
        params={
            "types": "R,G,H,N,S",
            "option": "",
            "count": "15",
            "includeOpenAndCloseDates": "true",
            "isWebsite": "true",
            "zipCode": zipCode,
        },
    )

    # check status code
    if response.status_code != 200:
        raise ValueError(
            "excepted 200 status for finding closest publix, was given "
            + str(response.status_code)
            + " for zip: "
            + zipCode
        )

    # range over response if successful
    for store_value in response.json()["Stores"]:
        # after the first iteration, return
        return [shave_zeros(store_value["KEY"]), store_value["NAME"]]


def grab_price(product_id, publix_collection):
    store_cookie = store_to_cookie(publix_collection[1])
    headers = {
        "Cookie": "Store={%22StoreName%22:%22"
        + store_cookie
        + "%22%2C%22StoreNumber%22:"
        + str(publix_collection[0])
        + "%2C%22Option%22:%22ACDFJNORTUV%22%2C%22ShortStoreName%22:%22"
        + store_cookie
        + "%22}"
    }
    sub_url = (
        "https://www.publix.com/shop-online/in-store-pickup/builder?baseProductID="
        + str(product_id)
    )

    response = requests.request("GET", f"{sub_url}", headers=headers, data={})

    # check status code
    if response.status_code != 200:
        raise ValueError(
            "excepted 200 status for grabbing product page, was given "
            + str(response.status_code)
            + " for product id: "
            + product_id
        )

    regex = r"&quot;Priceline1&quot;:&quot;[\$\d+\.]+"
    matches = re.finditer(regex, response.text, re.MULTILINE)
    # range over the match groups
    for matchNum, match in enumerate(matches, start=1):
        if matchNum == 2:
            break
    sub_price = match.group().split(";")[3]
    return sub_price


def grab_end_date(product_id, publix_collection):
    # create the store cookie sub value using the store name
    store_cookie = store_to_cookie(publix_collection[1])

    headers = {
        "Cookie": "Store={%22StoreName%22:%22"
        + store_cookie
        + "%22%2C%22StoreNumber%22:"
        + str(publix_collection[0])
        + "%2C%22Option%22:%22ACDFJNORTUV%22%2C%22ShortStoreName%22:%22"
        + store_cookie
        + "%22}"
    }
    sub_url = "https://www.publix.com/pd/" + str(product_id)
    response = requests.request("GET", f"{sub_url}", headers=headers, data={})

    # check status code
    if response.status_code != 200:
        raise ValueError(
            "excepted 200 status for grabbing product page, was given "
            + str(response.status_code)
            + " for product id: "
            + product_id
        )

    # prepare regex
    regex = r":&amp;quot;Valid Through [\w\s]+"

    # range over the match groups
    for matchNum, match in enumerate(
        re.finditer(r":&amp;quot;Valid Through [\w\s]+", response.text, re.MULTILINE),
        start=0,
    ):
        return match.group()


def remove_space_pubsub_name(pubsub):
    for i in range(0, len(pubsub.pubsub_name)):
        if pubsub.pubsub_name[i][-1] == " ":
            pubsub.pubsub_name[i] = pubsub.pubsub_name[i][:-1]
    return pubsub


def parse_publix_deli_page(zipCode):

    try:
        closest_publix = find_closest_publix(zipCode)
        # print("Store found: " + closest_publix[1])  # debug
    except:
        print(
            "an unexpected exception occured grabbing the closest publix at: " + zipCode
        )

    response = requests.request(
        "GET",
        "https://services.publix.com/api/v3/product/SearchMultiCategory?"
        + "storeNumber="
        + closest_publix[0]
        + "&sort=popularityrank+asc,+titlecopy+asc&rowCount=60&orderAheadOnly=true&facet=onsalemsg::On+Sale&categoryIdList=d3a5f2da-3002-4c6d-949c-db5304577efb",
        data="",
        headers={},
        params={},
    )

    if response.status_code != 200:
        raise ValueError(
            "excepted 200 status for grabbing on sale page, was given "
            + str(response.status_code)
        )
    pubsub = Pubsub()
    # find product valid thru date
    for product in response.json()[0]:
        if "Sub" in product["title"]:  # find subs only
            try:
                end_date = (
                    str(grab_end_date(product["Productid"], closest_publix))
                    .split("&amp;quot;Valid Through")[1]
                    .strip()
                )
                month_name = end_date.split(" ")[0]
                month_day = end_date.split(" ")[1]
                converted_month_number = convert_month_to_numerical(month_name)
                now = datetime.date.today()
                whole_sub_sale_date = (
                    str(now.month)
                    + "/"
                    + str(now.day)
                    + "/"
                    + str(now.year)
                    + "-"
                    + str(converted_month_number)
                    + "/"
                    + month_day
                    + "/"
                    + str(now.year)
                )
            except:
                print(
                    "an unexpected exception occured grabbing the end date of sub: "
                    + product["title"]
                )
            try:
                price = grab_price(product["Productid"], closest_publix).split("$")[1]
            except:
                print(
                    "an unexpected exception occured grabbing the price of sub: "
                    + product["title"]
                )

            sub_name = product["title"].replace("Publix", "").replace("Sub", "")

            filter_list = {
                "Boar&#39;s Head&reg;": "",
                "Boar&#39;s Head": "",
                "Boar&#39;s": "",
                "&amp": "&",
                "Chicken Tender": "Chicken Tenders",
            }

            # Go through the filtered list and replace the words with their values
            for filtered_words, replacements in filter_list.items():
                if filtered_words in sub_name:
                    sub_name = sub_name.replace(filtered_words, replacements)

            pubsub.pubsub_name.append(sub_name[1:-1])
            pubsub.price.append(str(price))
            temp_image_holder = str(product["productimages"]).split("-")
            pubsub.image_original.append(
                temp_image_holder[0] + "-600x600-" + temp_image_holder[2]
            )
            try:
                pubsub.date.append(whole_sub_sale_date)
            except:
                print(
                    "an unexpected exception occured appending the valid through (end date) to: "
                    + product["title"]
                )
    remove_space_pubsub_name(pubsub)

    for sub in range(0, len(pubsub.pubsub_name)):
        s3_utils.check_image(
            pubsub.pubsub_name[sub], pubsub.image_original[sub], my_bucket, pubsub
        )
    return pubsub


def shave_zeros(raw_store):
    store_id = ""
    for char in raw_store:
        # if there is a trailing zero in the store_id, don't include it
        if char != "0":
            store_id += str(char)

    return store_id


def store_to_cookie(store):
    return str(store).replace(" ", "%20")


if __name__ == "__main__":
    scrape_publix_job()
