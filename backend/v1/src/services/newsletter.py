import requests
import re
import json


def register_data(email: str, first_name: str, checked_subs):
    with open("services/mailgun.json") as loop:
        data = json.load(loop)
    api_key = data["api_key"]
    domain = data["domain"]
    checked_subs = [subs.replace(" ", "") for subs in checked_subs]
    files = {
        "subscribed": (None, "True"),
        "address": (None, email),
        "name": (None, first_name),
    }
    for sub in checked_subs:
        try:
            requests.post(
                "https://api.mailgun.net/v3/lists",
                auth=("api", api_key),
                data={
                    "address": f"{sub}@{domain}",
                    "description": f"Get notifications for {sub} subs!",
                    "name": f"{sub}",
                },
            )
        except:
            print(f"{sub} exists already, let's continue")
    """
    Let's make new mailing lists if they don't exist!
    """
    response_test = requests.get(
        "https://api.mailgun.net/v3/lists/pages",
        auth=("api", api_key),
    )
    mailing_lists_data = []
    mailing_lists = response_test.json()["items"]
    for index in mailing_lists:
        mailing_lists_data.append(index["address"])
    checked_subs = [subs.replace(" ", "") for subs in checked_subs]

    data = {}
    sub_list = []

    """
    Create a false and true fake dictionary, will be handy for updating someone's mailing list
    """
    for sub_domains in mailing_lists_data:
        for subs in checked_subs:
            if re.findall("^" + subs + "@", sub_domains):
                sub_list.append(str(sub_domains) + ":" + str(True))
            else:
                sub_list.append(str(sub_domains) + ":" + str(False))
    """
    Make sure there's no duplicates
    """
    sub_list = list(set(sub_list))

    """
    Using regex, remove the entries that contains our subs that have false data with them, only allowing true entries
    """
    for sub_names in sub_list:
        for sub_name in checked_subs:
            if re.findall("^" + sub_name + ".*:False$", sub_names):
                sub_list = list([val.replace(sub_names, "") for val in sub_list])
            else:
                continue
    """
    Removes empty spaces in our list
    """
    while "" in sub_list:
        sub_list.remove("")
    """
    Loops through the sub domain list,
    Search for true and false values and add a user to a mailing list if true, 
    Unsubscribe if false
    """
    for subs in sub_list:
        try:
            if re.findall("^.*:True$", subs):
                subs = subs.replace(":True", "")
                response = requests.post(
                    f"https://api.mailgun.net/v3/lists/{subs}/members",
                    files=files,
                    auth=("api", api_key),
                )
                print(response.json())

            elif re.findall("^.*:False$", subs):
                subs = subs.replace(":False", "")
                response = requests.put(
                    (f"https://api.mailgun.net/v3/lists/{subs}/members/{email}"),
                    auth=("api", api_key),
                    data={"subscribed": False, "name": first_name},
                )
                print(response.json())
        except:
            print("Could not find any data matching either true or false!")
    return "Completed adding to email!"
