from importlib.resources import Package
import json
from tkinter import Pack
import requests
from dotenv import load_dotenv
from os.path import join, dirname
import os
from discord_webhook import DiscordWebhook, DiscordEmbed
import jinja2

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


def create_html(pubsub):
    loader = jinja2.FileSystemLoader("./email_template.html")
    env = jinja2.Environment(loader=loader)
    template = env.get_template("")
    return template.render(
        zipcodes=pubsub.zipcodes,
        cities=pubsub.cities,
        closest_stores=pubsub.closest_stores,
        dates=pubsub.dates,
        prices=pubsub.prices,
        states=pubsub.states,
        pubsub_name=pubsub.pubsub_name,
    )


def send_email(pubsub, mailgun_obj):
    sub = pubsub.pubsub_name.lower().replace(" ", "")
    html_template = create_html(pubsub)
    sender_email = mailgun_obj.sender_email
    domain = mailgun_obj.domain
    api_key = mailgun_obj.mail_api_key
    response = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={
            "from": f"Pubsub-api {sender_email}",
            "to": [f"{sub}@{domain}"],
            "subject": f"Deal on {sub}",
            "html": html_template,
        },
    )
    print(response.json())


def send_email_and_webhook(pubsub, webhook, mailgun_obj):
    send_email(pubsub, mailgun_obj)
    webhook = DiscordWebhook(url=webhook)
    embed = DiscordEmbed(
        title="New sub on sale!",
        description=":tada:  A sub is on sale!\n"
        + pubsub.pubsub_name
        + " is on sale from: "
        + pubsub.date
        + ", for the price of $"
        + pubsub.price,
    )
    embed.set_image(url=pubsub.image)

    # add embed object to webhook
    webhook.add_embed(embed)

    response = webhook.execute()
