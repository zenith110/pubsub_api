from mailchimp3 import MailChimp
from services.mailchimp_api import key, username, list_id
from mailchimp_marketing.api_client import ApiClientError
import hashlib
from itertools import chain
import re


def hash_email(email: str):
    result = hashlib.md5(email.encode("utf-8")).hexdigest()
    return result


def create_interest(client, list_id: str, name: str):
    try:
        interest = client.lists.interest_categories.create(
            list_id, {"title": name, "type": "checkboxes"}
        )
        print("Made the interest group " + name)
        return interest
    except ApiClientError as error:
        print(
            "Failed to make interest group: " + name + "\nError: {}".format(error.text)
        )
        return


def make_category_id_json(interest_schema, sub_name: list, email: str, first_name: str):
    data_subs = []
    sub_names = []
    data = {
        "email_address": email,
        "status": "subscribed",
        "merge_fields": {"FNAME": first_name},
        "interests": {},
    }
    i = 0
    for i in range(0, len(interest_schema)):
        for j in range(0, len(sub_name)):
            if interest_schema[i]["name"] == sub_name[j]:
                id = interest_schema[i]["id"]
                data_subs.append(interest_schema[i]["name"] + ":" + str(id) + ":True")
                sub_names.append(interest_schema[i]["name"])
            else:
                id = interest_schema[i]["id"]
                data_subs.append(interest_schema[i]["name"] + ":" + str(id) + ":False")
                sub_names.append(interest_schema[i]["name"])
                # data["interests"][id] = False
    data_subs = list(set(data_subs))
    sub_names = list(set(sub_names))
    for i in range(0, len(data_subs)):
        for j in range(0, len(sub_name)):
            if re.findall("^" + sub_name[j] + ":[a-z0-9]*:False$", data_subs[i]):
                data_subs = list([val.replace(data_subs[i], "") for val in data_subs])
            else:
                continue

    while "" in data_subs:
        data_subs.remove("")

    for i in range(0, len(data_subs)):
        for j in range(0, len(sub_names)):
            if re.findall("True", data_subs[i]):
                # print(data_subs[i])
                data_subs = list(
                    [val.replace(sub_names[j] + ":", "") for val in data_subs]
                )
                data_subs = list([val.replace(":True", ": True") for val in data_subs])
            else:
                data_subs = list(
                    [val.replace(sub_names[j] + ":", "") for val in data_subs]
                )
                data_subs = list(
                    [val.replace(":False", ": False") for val in data_subs]
                )
    print(data_subs)

    for i in range(0, len(data_subs)):
        if re.findall("True", data_subs[i]):
            true = list([val.replace(": True", "") for val in data_subs])
            data["interests"][true[i]] = True
        elif re.findall("False", data_subs[i]):
            false = list([val.replace(": False", "") for val in data_subs])
            data["interests"][false[i]] = False

    return data


def get_category_id(interest_schema, sub_name):
    for i in range(0, len(interest_schema)):
        if interest_schema[i]["title"] == sub_name:
            id = interest_schema[i]["id"]
            return id
        else:
            continue


def register_data(email: str, first_name: str, checked_subs: list):

    client = MailChimp(key, username)

    """
    Adds provided first name with provided email  to pubsub mailing newsletter
    """

    all_interest = client.lists.interest_categories.all(list_id=list_id, get_all=False)
    try:
        interest = create_interest(client, list_id, "pubsub")
    except:
        print("Pubsub exists, let's keep moving!")

    hashed_email = hash_email(email.lower())
    all_interest = client.lists.interest_categories.all(list_id=list_id, get_all=True)
    pubsub = get_category_id(all_interest["categories"], "pubsub")
    if client.lists.members.get(list_id=list_id, subscriber_hash=hashed_email) == None:
        client.lists.members.create(
            list_id,
            {
                "email_address": email.lower,
                "status": "subscribed",
                "merge_fields": {"FNAME": first_name},
                "interest": pubsub,
            },
        )
        return "Added user to list and category!"
    else:
        print("User data exists, let's update their data!")
        hashed_email = hash_email(email.lower())
        all_interest = client.lists.interest_categories.all(
            list_id=list_id, get_all=True
        )

        pubsub = get_category_id(all_interest["categories"], "pubsub")
        for i in checked_subs:
            try:
                client.lists.interest_categories.interests.create(
                    list_id=list_id, category_id=pubsub, data={"name": i}
                )
            except:
                print("It exists, let's ignore")
                continue
        interests = client.lists.interest_categories.interests.all(
            list_id=list_id, category_id=pubsub, get_all=False
        )

        """
        Removes duplicates
        """

        id_data = make_category_id_json(
            interests["interests"], checked_subs, email, first_name
        )

        client.lists.members.update(list_id, hashed_email, id_data)
        return "Updated"
