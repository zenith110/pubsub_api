import docker
import schedule
import time
import json
import subprocess
from discord_webhook import DiscordWebhook
from datetime import datetime
from pytz import timezone
def discord_notification():
    with open("discord_hook") as discord_hook:
        data = json.load(discord_hook)

    tz = timezone("EST")
    now = datetime.now(tz)
    webhook_key = data["webhook_key"]
    up = DiscordWebhook(
                url=webhook_key,
                content="```Site  is up again! Done at:\n"
                + str(now.month)
                + "/"
                + str(now.day)
                + "/"
                + str(now.year)
                + " - "
                + str(now.hour)
                + ":"
                + str(now.minute) + "```"
            )
        up_response = up.execute()
"""
Pulls a container, specified by name
"""
def docker_pull(container_name: str, client: docker.from_env(), user_name):
    print("Pulling " + container_name + " from the repo now!")
    client.images.pull("zenith110/" + container_name)

"""
Logs into docker
"""
def docker_login():
    with open("dockerhub_login.json") as docker_login:
        login = json.load(docker_login)

    client = docker.from_env()

    username = login["Login"]["Username"]
    password = login["Login"]["Password"]

    client.login(username=username, password=password)
    return client

"""
Sets up a schedule that runs at midnight every day to check if a new container is available to download
""" 
def docker_checks():
    client = docker_login()
    docker_pull("pubsub-frontend", client)
    docker_pull("pubsub-backend", client)
    kill_all = subprocess.Popen(["killall", "docker-compose"])
    docker_compose = subprocess.Popen(["docker-compose", "up", "--build"])
    discord_notification()

if __name__ == "__main__":
    schedule.every().day.at("00:00").do(docker_checks)