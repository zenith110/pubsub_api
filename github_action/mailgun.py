import json
import requests
from dotenv import load_dotenv
from os.path import join, dirname
import os
from discord_webhook import DiscordWebhook, DiscordEmbed

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


def send_email(original_sub: str, dates: str, mailgun_obj):
    sub = original_sub.replace(" ", "")
    sender_email = mailgun_obj.sender_email
    domain = mailgun_obj.domain
    api_key = mailgun_obj.mail_api_key
    response = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={
            "from": f"Pubsub-api {sender_email}",
            "to": [f"{sub}@{domain}"],
            "subject": f"Deal on {sub} from {dates}",
            "text": f"Greetings from pubsub-api.dev! We're emailing to let you know that {original_sub} is on sale from {dates}",
        },
    )
    print(response.json())


def send_email_and_webhook(pubsub_name, pubsub_date, pubsub_price, pubsub_image, webhook, mailgun_obj):
    # send_email(pubsub_name, pubsub_date, mailgun_obj)
    webhook = DiscordWebhook(url=webhook)
    embed = DiscordEmbed(
        title="New sub on sale!",
        description=":tada:  A sub is on sale!\n"
        + pubsub_name
        + " is on sale from: "
        + pubsub_date
        + ", for the price of $"
        + pubsub_price,
    )
    embed.set_image(url=pubsub_image)

    # add embed object to webhook
    webhook.add_embed(embed)

    response = webhook.execute()
