from flask import Flask, render_template, abort, jsonify
import connect_db
import json


def random_subs():
    try:
        connection = connect_db.connect()
        cur = connection.cursor()
        # Checks to see if the name exist in the record, then grabs a random row from that column limiting it to one.
        command = "SELECT pubsub_name, dates, on_sale, price, image FROM {table} WHERE pubsub_name is NOT NULL ORDER BY random() DESC LIMIT 1"
        query = cur.execute(command.format(table=connect_db.get_table()))

        # Fetches us all the rows so we can grab data from each
        records = cur.fetchall()

        for row in records:
            subname = row[0]
            last_on_sale = row[1]
            on_sale = row[2]
            price = row[3]
            image = row[4]

        # Creates a dictionary
        data = {}

        # Creates a primary catagory
        data["random_sub"] = []

        # Create a default JSON structure
        data["random_sub"].append(
            {
                "sub_name": subname.lower(),
                "last_sale": last_on_sale,
                "status": on_sale,
                "price": price,
                "image": image,
            }
        )

        sub_info = jsonify(data["random_sub"])
        sub_info.headers.add("Access-Control-Allow-Origin", "*")
        return sub_info
    except:
        return abort(404)
