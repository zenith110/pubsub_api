import psycopg2
import json
import os
import requests
from PySide2 import QtWidgets, QtCore, QtGui
from ui import uploader
import connect_db
from services import mailgun
from discord_webhook import DiscordWebhook, DiscordEmbed

class uploader(uploader.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(uploader, self).__init__()
        self.setupUi(self)
        self.upload.clicked.connect(self.add_entry)
        self.delete_2.clicked.connect(self.delete_entry)

    def delete_entry(self):
        sub_name = self.sub_name.text()
        dates = self.date.text()
        on_sale = self.on_sale.text()
        sub_name = sub_name.replace(" ", "-").lower()
        price = self.price.text()
        image = self.image.text()

        connection = connect_db.connect()
        cur = connection.cursor()

        print("Deleting data on " + sub_name + "!")
        cur.execute(
            "DELETE FROM "
            + connect_db.get_table()
            + " WHERE pubsub_name LIKE '%"
            + sub_name
            + "%'"
        )

        connect_db.close(connection)

    # Updates and inserts automatically
    def add_entry(self):
        sub_name = self.sub_name.text()
        dates = self.date.text()
        on_sale = self.on_sale.text()
        sub_name = sub_name.replace(" ", "-").lower()
        original = self.sub_name.text().lower()
        price = self.price.text()
        image = self.image.text()

        connection = connect_db.connect()

        cur = connection.cursor()
        # Checks to see if that row exist
        exist_query = (
            "select exists(select 1 from {table} where pubsub_name ='{sub}' limit 1)"
        )
        exist_check = cur.execute(
            exist_query.format(table=connect_db.get_table(), sub=sub_name)
        )
        count = cur.fetchone()[0]
        # If our data returns true, update the status and dates
        if count == True:
            print("There exist a version of " + sub_name + " now updating!")
            update_string = "Update {table} SET on_sale = '{on_sale}', dates = '{dates}', price = '{price}', image = '{image}' WHERE pubsub_name = '{sub}'"
            update_query = cur.execute(
                update_string.format(
                    table=connect_db.get_table(),
                    on_sale=on_sale,
                    dates=dates,
                    price=price,
                    image = image,
                    sub=sub_name,
                )
            )
            # Sends an email out if a sub is now on sale
            if on_sale == "True":
                mailgun.send_email(original, dates)
                with open("webhook.json") as webhook_data:
                    data = json.load(webhook_data)
                webhook = DiscordWebhook(url=data["webhook"])
                embed = DiscordEmbed(title = "New sub on sale!", description = "@810362326954934283 :tada:  A current sub is on sale!\n" + sub_name + " is on sale from: " + dates + ", for the price of " + price)
                embed.set_image(url = image)
                
                # add embed object to webhook
                webhook.add_embed(embed)

                response = webhook.execute()
        else:
            print("This sub doesn't exist, now adding!")
            # Inserts the data into each column
            cur.execute(
                "INSERT INTO "
                + connect_db.get_table()
                + "(pubsub_name, dates, on_sale, price, image) VALUES (%s, %s, %s, %s, %s)",
                (sub_name, dates, on_sale, price, image),
            )
            if on_sale == "True":
                print("Sub is on sale")
                mailgun.send_email(original, dates)
                with open("webhook.json") as webhook_data:
                    data = json.load(webhook_data)
                webhook = DiscordWebhook(url=data["webhook"])
                embed = DiscordEmbed(title = "New sub on sale!", description = ":tada:  @810362326954934283 A sub is on sale!\n" + sub_name + " is on sale from: " + dates + ", for the price of " + price)
                embed.set_image(url = image)
                               
                # add embed object to webhook
                webhook.add_embed(embed)

                response = webhook.execute()

        connect_db.close(connection)


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    qt_app = uploader()
    qt_app.show()
    app.exec_()
