"""
Fetches the latest pub sub deal 
"""
import requests


class RandomSub:
    def __init__(self):
        self.innards = None
        self.sub_name = ""
        self.last_sale = ""
        self.on_sale = ""
        self.price = ""
        self.image = ""
        self.status_code = ""


def GetAllSubs():
    sub = RandomSub()
    try:
        url = "https://api.pubsub-api.dev/allsubs/"
        response = requests.get(url).json()
        sub_names = []
        for i in range(len(response)):
            sub_names.append(response[i]["name"])
        sub.sub_name = ", ".join(sub_names)
        sub.status_code = "200"
        return sub
    except:
        sub.status_code = "404"
        return sub

def GetPubSub(sub_name: str):
    sub_name = sub_name.replace(" ", "-")
    url = "https://api.pubsub-api.dev/subs/?name=" + sub_name
    response = requests.get(url)
    try:
        response = response.json()
        sub = RandomSub()
        sub.sub_name = response[0]["sub_name"]
        sub.last_sale = response[0]["last_sale"]
        sub.status = response[0]["status"]
        sub.price = response[0]["price"]
        sub.image = response[0]["image"]
        sub.status_code = "OK"
        return sub
    except:
        sub = RandomSub()
        if response.status_code == 503:
            sub.status_code = "503"
            return sub
        elif response.status_code == "404":
            sub.status_code = "404"
            return sub


def EmptySubInput():
    sub = RandomSub()
    url = "https://api.pubsub-api.dev/subs/?name=random"
    response = requests.get(url)
    try:
        response = response.json()
        sub.sub_name = response[0]["sub_name"]
        sub.last_sale = response[0]["last_sale"]
        sub.status = response[0]["status"]
        sub.price = response[0]["price"]
        sub.image = response[0]["image"]
        sub.status_code = "200"
        return sub
    except:
        sub.status_code = "503"
        return sub