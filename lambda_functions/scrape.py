from copy import Error
from logging import error
from botocore.retries import bucket
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.command import Command
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import boto3
import connect_db
from datetime import datetime
import mailgun
from discord_webhook import DiscordWebhook, DiscordEmbed
import http
import socket
import os
from os.path import join, dirname
import time

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


class Pubsub:
    def __init__(self) -> None:
        self.names = []
        self.dates = []
        self.prices = []


class DatabaseObject:
    def __init__(self) -> None:
        self.user = ""
        self.password = ""
        self.host = ""
        self.port = ""
        self.database = ""
        self.table = ""


def run_driver():
    chrome_driver = "chromedriver.exe"
    s3 = boto3.resource(
        service_name="s3",
        region_name="us-east-2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--incognito")
    options.add_argument("--deny-permission-prompts")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    driver = webdriver.Chrome(options=options)
    bucket_name = os.getenv("BUCKET_NAME")
    my_bucket = s3.Bucket(bucket_name)

    db_object = DatabaseObject()
    db_object.user = os.getenv("USERNAME_DB")
    db_object.password = os.getenv("PASSWORD")
    db_object.host = os.getenv("HOST")
    db_object.port = os.getenv("PORT")
    db_object.database = os.getenv("DATABASE")
    db_object.table = os.getenv("TABLE")
    """
    Begin the web driver by starting on the weekly add
    """
    try:
        """
        Starts at the main publix page
        """
        driver.get("https://www.publix.com/")

        """
        Clicks the various elements to access the deli page
        """
        print("Let's access the deli page!")
        try:
            dropdown_button = driver.find_element_by_xpath(
                '//*[@id="header"]/div/button'
            ).click()
            weekly_special_opener = driver.find_element_by_xpath(
                '//*[@id="body-wrapper"]/div/header/div[1]/div[2]/div/div[2]/div[1]/nav/ul/li[2]/div/a'
            )
            weekly_special_opener.click()
            try:
                weekly_special = driver.find_element_by_xpath(
                    '//*[@id="main"]/section/div/div[1]/div/a'
                )
                weekly_special.click()
            except Error:
                print(Error)
                return "Failed!"
            try:
                print("Waiting 5 seconds to load the store page.")
                time.sleep(5)
                store_selector_button = driver.find_element_by_xpath(
                    '//*[@id="main"]/div[4]/div[2]/div/div/button'
                )
                store_selector_button.click()
                use_current_location = driver.find_element_by_xpath(
                    '//*[@id="body-wrapper"]/div[2]/div/div/div[2]/div[1]/form/div[3]/button/span[1]'
                ).click()
                search_store = driver.find_element_by_xpath(
                    '//*[@id="input_ZIPorCity,Stateorstorenumber109"]'
                )
                search_store.send_keys(os.getenv("ZIPCODE"))
                search_store.send_keys(Keys.RETURN)
                """
                Waits a bit for the store_lookup_button to load
                """
                print("Waiting 5 seconds for store lookup button to load")
                time.sleep(5)
                store_lookup_button = driver.find_element_by_xpath(
                    '//*[@id="body-wrapper"]/div[2]/div/div/div[2]/div[1]/form/div[1]/button'
                ).click()
                first_store = driver.find_element_by_xpath(
                    '//*[@id="body-wrapper"]/div[2]/div/div/div[2]/div[2]/div/ul/li[1]/div/button'
                ).click()
            except Error:
                print(Error)
                return "Failed!"
            """
            Waits for the weekly special page to load
            """
            print("Waiting for weekly ad page to load")
            time.sleep(5)
            """
            Switches the driver over to the deli page of weekly specials
            """
            driver.get(driver.current_url + "/deli")
            """
            Grabs the url and let's us parse the contents of the page.
            """
            deli_page_url = driver.current_url
            deli_page = requests.get(deli_page_url)
            deli_page_content = deli_page.content
        except Error:
            print(Error)
            return "Failed!"
        try:
            print("Let's scrape the page for data now!")
            """
            Finds the various properties of the subs
            """
            sub_price = driver.find_elements_by_class_name("sub-title")
            all_items = driver.find_elements_by_class_name("card-title")
            dates = driver.find_elements_by_class_name("text-block-default")
            """
            Creates a pubsub object to print at the end
            """
            pubsub = Pubsub()
            """
            Scrapes the substring if they're 5.99 or 6.99
            """
            for price in sub_price:
                if (
                    "5.99 EACH" in price.text
                    or "6.99 EACH" in price.text
                    or "6.99" in price.text
                ):
                    pubsub.prices.append(price.text)
            """
            If we fail to get any price data, fail and re-run
            """
            if len(pubsub.prices) <= 0:
                return "Failed!"
            """
            Replaces aspects that we don't want for the subs
            """
            pubsub.prices = [price.replace("EACH", "") for price in pubsub.prices]
            pubsub.prices = list(
                set([price.replace(" ", "") for price in pubsub.prices])
            )

            """
            Finds the dates that contain valid within
            """
            today = datetime.today()
            for date in dates:
                if (
                    "Valid " in date.text
                    and str(today.month) + "/" in date.text
                    and str(today.month - 1) + "/" not in date.text
                ):
                    pubsub.dates.append(date.text)
            """
            Cleans up the dates strings
            """
            pubsub.dates = [date.replace("Valid", "") for date in pubsub.dates]
            pubsub.dates = list(set([date.replace(" ", "") for date in pubsub.dates]))
            """
            Checks for Whole sub and appends to a new list
            """
            for items in all_items:
                if "Whole Sub" in items.text:
                    pubsub.names.append(items.text)
            """
            Removes all the spaces in the names list
            """
            while "" in pubsub.names:
                pubsub.names.remove("")
            plural_subs = ["chicken-tender"]
            """
            Removes unnecessary text from the subs names
            """
            pubsub.names = [sub.replace("Whole Sub", "") for sub in pubsub.names]
            pubsub.names = [sub.replace("Publix Deli", "") for sub in pubsub.names]
            pubsub.names = [sub.replace("Board's Head", "") for sub in pubsub.names]
            aws_names = [sub.lower() for sub in pubsub.names]
            removed_last_char_aws_names = [x[1:-1] for x in aws_names]
            removed_last_char_aws_names = [
                x.replace(" ", "-") for x in removed_last_char_aws_names
            ]
            """
            Loops through a list in order to find singular subs that are plural in the db
            """
            for chars in range(0, len(removed_last_char_aws_names)):
                for names in plural_subs:
                    if removed_last_char_aws_names[chars] in names:
                        print("Found the names!")
                        removed_last_char_aws_names[chars] = names + "s"
            # pubsub.names = [sub.replace(" ", "") for sub in pubsub.names]
        except Error:
            print(Error)
            return "Failed!"
        images = []
        print(vars(pubsub))
        connection = connect_db.connect(db_object)
        cur = connection.cursor()
        """
        Set all the subs to false
        """
        make_all_subs_false = "Update {table} SET on_sale=False"
        update_query = cur.execute(
            make_all_subs_false.format(
                table=connect_db.get_table(db_object),
            )
        )
        for i in range(0, len(pubsub.names)):
            try:
                """
                Retrives the images from AWS S3
                """
                for object_summary in my_bucket.objects.filter(
                    Prefix=removed_last_char_aws_names[i]
                ):
                    images.append(
                        "https://pubsub-images.s3.us-east-2.amazonaws.com/"
                        + object_summary.key
                    )
                """
                Splits the dates into months and days to be used as a datetime
                """
                split_dates = pubsub.dates[i].split("-")
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
                        table=connect_db.get_table(),
                        sub=removed_last_char_aws_names[i].lower(),
                    )
                )
                count = cur.fetchone()[0]
                print(count)
                """
                If the sub currently exists, check to see if we're within the period of the sale
                """
                if count == True:
                    """
                    Checks to see if we are past the sale date
                    """
                    if days_past_starting.days > 0 and days_left_till_end.days <= 0:
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
                                dates=pubsub.dates[i],
                                price=pubsub.prices[i],
                                image=images[i],
                                sub=removed_last_char_aws_names[i],
                            )
                        )
                        if on_sale == "True":
                            mailgun.send_email(pubsub.names[i], pubsub.dates[i])
                            webhook = DiscordWebhook(url=os.getenv("WEBHOOK"))
                            embed = DiscordEmbed(
                                title="New sub on sale!",
                                description=":tada:  A sub is on sale!\n"
                                + pubsub.names[i]
                                + " is on sale from: "
                                + pubsub.dates[i]
                                + ", for the price of $"
                                + pubsub.prices[i],
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
                                dates=pubsub.dates[i],
                                price=pubsub.prices[i],
                                image=images[i],
                                sub=removed_last_char_aws_names[i],
                            )
                        )
                else:
                    if days_past_starting.days > 0 and days_left_till_end.days <= 0:
                        # Inserts the data into each column
                        cur.execute(
                            "INSERT INTO "
                            + connect_db.get_table()
                            + "(pubsub_name, dates, on_sale, price, image) VALUES (%s, %s, %s, %s, %s)",
                            (
                                pubsub.names[i].replace(" ", "-").lower(),
                                pubsub.dates[i],
                                True,
                                pubsub.prices[i],
                                images[i],
                            ),
                        )
                        """
                        If the sub is currently on sale, send out an email and a web hook alert to the discord
                        """
                        if on_sale == "True":
                            print("Sub is on sale")
                            mailgun.send_email(pubsub.names[i], pubsub.dates[i])

                            webhook = DiscordWebhook(url=os.getenv("WEBHOOK"))
                            embed = DiscordEmbed(
                                title="New sub on sale!",
                                description=":tada:  A sub is on sale!\n"
                                + pubsub.names[i]
                                + " is on sale from: "
                                + pubsub.dates[i]
                                + ", for the price of $"
                                + pubsub.prices[i],
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
                                dates=pubsub.dates[i],
                                price=pubsub.prices[i],
                                image=images[i],
                                sub=pubsub.names[i].replace(" ", "-").lower(),
                            )
                        )
            except:
                return "Failed"

    except Error:
        print(Error)
        return "Failed!"


if __name__ == "__main__":
    driver_run = run_driver()
    """
    If lambda fails, rerun till it succeedes.
    """
    while driver_run == "Failed!":
        print("Failed! Re-running....")
        run_driver()
