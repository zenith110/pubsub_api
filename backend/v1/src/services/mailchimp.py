from mailchimp3 import MailChimp
from services.mailchimp_api import key, username, list_id
from mailchimp_marketing.api_client import ApiClientError
import hashlib
from itertools import chain
import re


def hash_email(email: str):
    result = hashlib.md5(email.encode("utf-8")).hexdigest()
    return result


def create_interest(client, list_id: str, checked_subs: list):
    try:
        interest = client.lists.interest_categories.create(
            list_id, {"title": checked_subs, "type": "checkboxes"}
        )
        print("Made the interest group " + checked_subs)
        return interest
    except ApiClientError as error:
        print(
            "Failed to make interest group: "
            + checked_subs
            + "\nError: {}".format(error.text)
        )
        return


def make_category_id_bool_json(interest_schema, sub_name):
    data = []
    for i in range(0, len(interest_schema)):
        if interest_schema[i]["title"] == sub_name:
            id = interest_schema[i]["id"]
            print("Found the sub!\n")
            print(sub_name + " id is: " + str(interest_schema[i]["id"] + "\n"))
            bool_data = "true"
            data.append(bool_data + "-" + str(i))
            return data
        else:
            print(
                str(interest_schema[i]["title"] + " is not what we're looking for!\n")
            )
            bool_data = "false"
            data.append(bool_data + "-" + str(i))
            continue
        return data


def make_category_id_json(interest_schema, sub_name):
    data = []
    for i in range(0, len(interest_schema)):
        if interest_schema[i]["title"] == sub_name:
            id = interest_schema[i]["id"]
            data.append(str(id))
            return data
        else:
            id = interest_schema[i]["id"]
            data.append(id)
            continue
        return data


def get_category_id(interest_schema, sub_name):
    for i in range(0, len(interest_schema)):
        if interest_schema[i]["title"] == sub_name:
            id = interest_schema[i]["id"]
            return id
        else:
            continue


def register_data(email: str, first_name: str, checked_subs: list):
    id_data = []
    print("Email is: " + email + "\nName is: " + first_name)
    client = MailChimp(key, username)
    print(checked_subs)
    """
    Adds provided first name with provided email  to pubsub mailing newsletter
    """
    print("Now printing all the interest categories")
    all_interest = client.lists.interest_categories.all(list_id=list_id, get_all=False)
    for i in range(0, len(checked_subs)):
        id = get_category_id(all_interest["categories"], checked_subs[i])
        id_data.append(id)

    for i in checked_subs:
        if i == None:
            print("Interest doesn't exist, let's make it!")
            interest = create_interest(client, list_id, checked_subs[i])
            print(type(interest))
        else:
            print("Interests exist, let's get out!")
            break
    hashed_email = hash_email(email)
    if client.lists.members.get(list_id=list_id, subscriber_hash=hashed_email) == None:
        client.lists.members.create(
            list_id,
            {
                "email_address": email,
                "status": "subscribed",
                "merge_fields": {"FNAME": first_name},
                "interest": checked_subs,
            },
        )
        print(checked_subs)
        print("Added " + first_name + " and " + email + " to the sub newsletter!")
        return "Added user to list and category!"
    else:
        print("User data exists, let's update their data!")
        # hashed_email = hash_email(email)
        # all_interest = client.lists.interest_categories.all(list_id = list_id, get_all=False)
        # sub_results_id = []
        # sub_results_id_bool = []
        # """
        # Removes duplicates
        # """
        # for i in checked_subs:
        #     id_data = make_category_id_json(all_interest["categories"], i)
        #     sub_results_id.append(list(set(id_data)))

        # for i in checked_subs:
        #     id_data = make_category_id_bool_json(all_interest["categories"], i)
        #     sub_results_id_bool.append(list(set(id_data)))
        # """
        # Turns our 2D array into a singular one
        # """
        # sub_results_id = list(chain.from_iterable(sub_results_id))
        # sub_results_id_bool = list(chain.from_iterable(sub_results_id_bool))
        # sub_results_id_bool = [s[:-1] for s in sub_results_id_bool]
        # sub_results_id_bool = [s.replace("-", "") for s in sub_results_id_bool]
        # print(sub_results_id_bool)
        # print(sub_results_id)
        # data = {
        #      "email_address": email,
        #             "status": "subscribed",
        #             "merge_fields": {"FNAME": first_name},
        #             "interests": [

        #             ]
        # }

        # for i in range(0, len(sub_results_id)):
        #     print(data["interests"])

        # print(data)
        # for i in range(0, len(checked_subs)):
        #     client.lists.members.update(list_id, hashed_email,
        #         data
        #     )
        # return "Updated"
