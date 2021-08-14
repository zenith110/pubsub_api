from botocore.retries import bucket
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.command import Command
from bs4 import BeautifulSoup
import os
import boto3
import connect_db
from datetime import datetime
import mailgun
from discord_webhook import DiscordWebhook, DiscordEmbed
import http
import socket


def get_status(driver):
    try:
        driver.execute(Command.STATUS)
        return "Alive"
    except (socket.error, http.client.CannotSendRequest):
        return "Dead"


def run_driver():
    chrome_driver = "chromedriver.exe"
    options = webdriver.ChromeOptions()
    s3 = boto3.resource(
        service_name="s3",
        region_name="us-east-2",
        aws_access_key_id=os.environ.get("aws_access_key_id"),
        aws_secret_access_key=os.environ.get("aws_secret_access_key"),
    )

    driver = webdriver.Chrome(chrome_options=options, executable_path=chrome_driver)
    bucket_name = os.environ.get("bucket_name")
    my_bucket = s3.Bucket(bucket_name)
    """
    Begin the web driver by starting on the weekly add
    """
    try:
        driver.get("https://www.publix.com/savings/weekly-ad")

        deli_page_redirect = driver.get(driver.current_url + "/deli")
        deli_page_url = driver.current_url
        deli_page = requests.get(deli_page_url)
        deli_page_content = deli_page.content
        try:
            """
            Finds the various properties of the subs
            """
            sub_price = driver.find_elements_by_class_name("sub-title")
            all_items = driver.find_elements_by_class_name("card-title")
            dates = driver.find_elements_by_class_name("text-block-default")
            price_list = []
            """
            Scrapes the substring if they're 5.99 or 6.99
            """
            for price in sub_price:
                if "5.99 EACH" in price.text or "6.99 EACH" in price.text:
                    price_list.append(price.text)
            """
            Replaces aspects that we don't want for the subs
            """
            price_list = [price.replace("EACH", "") for price in price_list]
            price_list = [price.replace(" ", "") for price in price_list]
            subs = []
            filtered_dates = []
            """
            Finds the dates that contain valid within
            """
            for date in dates:
                if "Valid " in date.text:
                    filtered_dates.append(date.text)
            """
            Cleans up the dates strings
            """
            filtered_dates = [date.replace("Valid", "") for date in filtered_dates]
            filtered_dates = [date.replace(" ", "") for date in filtered_dates]
            all_names = []
            """
            Checks for Whole sub and appends to a new list
            """
            for items in all_items:
                if "Whole Sub" in items.text:
                    all_names.append(items.text)
            """
            Removes all the spaces in the names list
            """
            while "" in all_names:
                all_names.remove("")
            """
            Removes unnecessary text from the subs names
            """
            all_names = [sub.replace("Whole Sub", "") for sub in all_names]
            all_names = [sub.replace("Publix Deli", "") for sub in all_names]
            all_names = [sub.replace("Board's Head", "") for sub in all_names]
            all_names = [sub.replace(" ", "") for sub in all_names]
            aws_names = [sub.lower() for sub in all_names]
        except:
            print("could not find any data, sorry!")
        if len(all_names) <= 0:
            print("Could not get any text")
            return -1
        else:
            print(all_names)
        if get_status(driver) == "Alive":
            print("Process is still going, continue!")
        elif get_status(driver) == "Dead":
            print("Process has quit, stop and rerun!")
            return -1
        images = []

        connection = connect_db.connect()
        cur = connection.cursor()
        """
        Set all the subs to false
        """
        make_all_subs_false = "Update {table} SET on_sale=False"
        update_query = cur.execute(
            make_all_subs_false.format(
                table=connect_db.get_table(),
            )
        )
        for i in range(0, len(all_names)):
            try:
                """
                Retrives the images from AWS S3
                """
                for object_summary in my_bucket.objects.filter(Prefix=aws_names[i]):
                    images.append(
                        "https://pubsub-images.s3.us-east-2.amazonaws.com/"
                        + object_summary.key
                    )
                """
                Splits the dates into months and days to be used as a datetime
                """
                split_dates = filtered_dates[i].split("-")
                start_date_month = split_dates[0].split("/")[0]
                start_date_day = split_dates[0].split("/")[1]
                end_date = split_dates[1]
                end_date_month = split_dates[1].split("/")[0]
                end_date_day = split_dates[1].split("/")[1]
                """
                Creates the datetime objects from the dated provided above
                """
                current_date = datetime.now()
                current_year = current_date.year
                end_date_datetime = datetime(
                    int(current_year), int(end_date_month), int(end_date_day)
                )
                start_date_dateime = datetime(
                    int(current_year), int(start_date_month), int(start_date_day)
                )

                """
                Creates the days left till the sale is over, and how long the sale currently been going on for.
                """
                days_left_till_end = current_date - end_date_datetime
                days_past_starting = current_date - start_date_dateime

                exist_query = "select exists(select 1 from {table} where pubsub_name ='{sub}' limit 1)"
                exist_check = cur.execute(
                    exist_query.format(
                        table=connect_db.get_table(), sub=all_names[i].lower()
                    )
                )
                count = cur.fetchone()[0]
                """
                If the sub currently exists, check to see if we're within the period of the sale
                """
                if count == True:
                    """
                    Checks to see if we are past the sale date
                    """
                    if days_past_starting.days > 0 and days_left_till_end.days < 0:
                        on_sale = "True"
                        """
                        Resets all the current subs which are 
                        """

                        cur.execute(update_string.format())
                        update_string = "Update {table} SET on_sale = '{on_sale}', dates = '{dates}', price = '${price}', image = '{image}' WHERE pubsub_name = '{sub}'"
                        update_query = cur.execute(
                            update_string.format(
                                table=connect_db.get_table(),
                                on_sale=on_sale,
                                dates=filtered_dates[i],
                                price=price_list[i],
                                image=images[i],
                                sub=all_names[i].replace(" ", "-").lower(),
                            )
                        )
                        if on_sale == "True":
                            mailgun.send_email(all_names[i], filtered_dates[i])
                            webhook = DiscordWebhook(url=os.environ.get("webhook"))
                            embed = DiscordEmbed(
                                title="New sub on sale!",
                                description=":tada:  A sub is on sale!\n"
                                + all_names[i]
                                + " is on sale from: "
                                + filtered_dates[i]
                                + ", for the price of $"
                                + price_list[i],
                            )
                            embed.set_image(url=images[i])

                            # add embed object to webhook
                            webhook.add_embed(embed)

                            response = webhook.execute()
                    else:
                        on_sale = "False"
                        update_string = "Update {table} SET on_sale = '{on_sale}', dates = '{dates}', price = '${price}', image = '{image}' WHERE pubsub_name = '{sub}'"
                        update_query = cur.execute(
                            update_string.format(
                                table=connect_db.get_table(),
                                on_sale=on_sale,
                                dates=filtered_dates[i],
                                price=price_list[i],
                                image=images[i],
                                sub=all_names[i].replace(" ", "-").lower(),
                            )
                        )
                else:
                    if days_past_starting.days > 0 and days_left_till_end.days < 0:
                        # Inserts the data into each column
                        cur.execute(
                            "INSERT INTO "
                            + connect_db.get_table()
                            + "(pubsub_name, dates, on_sale, price, image) VALUES (%s, %s, %s, %s, %s)",
                            (
                                all_names[i].replace(" ", "-").lower(),
                                filtered_dates[i],
                                True,
                                price_list[i],
                                images[i],
                            ),
                        )
                        """
                        If the sub is currently on sale, send out an email and a web hook alert to the discord
                        """
                        if on_sale == "True":
                            print("Sub is on sale")
                            mailgun.send_email(all_names[i], filtered_dates[i])

                            webhook = DiscordWebhook(url=os.environ.get("webhook"))
                            embed = DiscordEmbed(
                                title="New sub on sale!",
                                description=":tada:  A sub is on sale!\n"
                                + all_names[i]
                                + " is on sale from: "
                                + filtered_dates[i]
                                + ", for the price of $"
                                + price_list[i],
                            )
                            embed.set_image(url=images[i])

                            """
                            add embed object to webhook
                            """
                            webhook.add_embed(embed)

                            response = webhook.execute()
                    else:
                        on_sale = "False"
                        update_string = "Update {table} SET on_sale = '{on_sale}', dates = '{dates}', price = '${price}', image = '{image}' WHERE pubsub_name = '{sub}'"
                        update_query = cur.execute(
                            update_string.format(
                                table=connect_db.get_table(),
                                on_sale=on_sale,
                                dates=filtered_dates[i],
                                price=price_list[i],
                                image=images[i],
                                sub=all_names[i].replace(" ", "-").lower(),
                            )
                        )
            except:
                print("Could not update the information!")

    except:
        print("Could not complete operation")


if __name__ == "__main__":
    run_driver()
