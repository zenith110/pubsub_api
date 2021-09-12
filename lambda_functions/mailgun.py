import requests
from dotenv import load_dotenv
from os.path import join, dirname
import os

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
import json


def send_email(original_sub: str, dates: str):
    sub = original_sub.replace(" ", "")

    domain = os.getenv("DOMAIN")
    api_key = os.getenv("API_KEY")
    response = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={
            "from": "Pubsub-api email.pubsub.api@gmail.com",
            "to": [f"{sub}@{domain}"],
            "subject": f"Deal on {sub} from {dates}",
            "text": f"Greetings from pubsub-api.dev! We're emailing to let you know that {original_sub} is on sale from {dates}",
        },
    )
    print(response.json())
