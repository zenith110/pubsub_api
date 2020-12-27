import json
from twilio.rest import Client


def sms(connect_db, sub_name, date):
    # Opens up the twillo cred file
    with open("services/twillo.json", "r") as cred:
        data = json.load(cred)

    # Parses the json for the needed information
    account = data["ACCOUNT_SID"]
    token = data["AUTH_TOKEN"]
    serive_sid = data["SERVICE_SID"]
    # Connects the client so we can send messages
    client = Client(account, token)
    # Establishes connection and does database things
    connection = connect_db.connect()
    cur = connection.cursor()
    # Queries only for non null phone numbers
    query = "SELECT phone_number FROM {table} WHERE phone_number is not null"
    cur.execute(query.format(table=connect_db.get_table()))
    # Grabs data from query
    records = cur.fetchall()
    # Loops through the tuple to afix the phone number to message recipent
    for index, numbers in enumerate(records):
        phone_number = "+1" + str(numbers[index])
        notification = client.notify.services(serive_sid).notifications.create(
            # We recommend using a GUID or other anonymized identifier for Identity
            to_binding='{"binding_type":"sms", "address":"' + phone_number + '"}',
            body="Hello there from pubsub-api.dev! Reaching out to you that "
            + sub_name
            + " is on sale from "
            + date,
        )
