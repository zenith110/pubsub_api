from typing import ClassVar
import requests
import re
import json
import os
def send_email_first_time(domain_name: str, sender: str, recipent: str, sub_sales: list, first_name: str):
    return requests.post(
        f"https://api.mailgun.net/v3/{domain_name}/messages",
        auth=("api", "YOUR_API_KEY"),
        data={"from": f"Pubsub Api  {sender}",
              "to": f"{recipent}",
              "subject": "Your first pubsub-api newsletter!",
              "text": f"Hello {first_name}, \nThank you for registering for your first newsletter! \nThe current subs that you picked that are on sale are: {sub_sales}"})

def check_email_in_mailing_list(domain_name: str, api_key: str, email: str) -> bool:
    response = requests.get(f"https://api.mailgun.net/v3/lists/LIST@{domain_name}/members/pages",
        auth=('api', f"{api_key}"))
    for data in response["items"]:
        if(data["address"] == email):
            return True
        else:
            return False

def register_data(email: str, first_name: str, checked_subs, email_object):
    api_key = email_object.api_key
    domain = email_object.domain
    sender = email_object.sender
    overall_mailing_list = email_object.overall
    checked_subs = [subs.replace(" ", "") for subs in checked_subs]
    files = {
        "subscribed": (None, "True"),
        "address": (None, email),
        "name": (None, first_name),
    }

    for sub in checked_subs:
        try:
            """
            Let's make new mailing lists if they don't exist!
            """
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
    """
    Checks to see if the user is currently in the global list, if they currently are
    """
    user_email_check = check_email_in_mailing_list(domain, api_key, email)
    if(user_email_check is True):
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
    else:
        # Adds the users to the mailing lists for the specific subs
        # Adds the user to the general mailing list
        # Sends out an email for the first time welcoming them
        # And include sub data
        mailing_dates_names = []
        first_time_general_mailing_list = requests.post( f"https://api.mailgun.net/v3/lists/{overall_mailing_list}/members",
                        files=files,
                        auth=("api", api_key))
        subs_list = requests.get("https://api.pubsub-api.dev/onsale/").json()
        for subs in sub_list:
            try:
                if re.findall("^.*:True$", subs):
                    subs = subs.replace(":True", "")
                    response = requests.post(
                        f"https://api.mailgun.net/v3/lists/{subs}/members",
                        files=files,
                        auth=("api", api_key),
                    )
        
            except:
                print("Could not find any data matching either true or false!")
        for subs in checked_subs:
            for sub in subs_list:
                if(subs == sub["name"]):
                    mailing_dates_names.append(sub["name"] + " On sale from: " + sub["last_on_sale"])
                else:
                    continue
        # Join back all the sub names for the news letter!
        sub_special_dates = ",".mailing_dates_names.join()
        send_email_first_time(domain, sender, email, sub_special_dates, first_name)
    return "Completed adding to mailing lists!"
