import connect_db
from flask import Flask, render_template, request, redirect, jsonify, abort
import json


def sub_runner_checker(subname, db_object):
    try:
        connection = connect_db.connect(db_object)
        cur = connection.cursor()
        # Checks to see if the name exist in the record, then grabs a random row from that column limiting it to one.
        try:
            command = "SELECT pubsub_name, dates, on_sale, price, image FROM {table} WHERE pubsub_name = '{name}' ORDER BY dates DESC LIMIT 1"
            query = cur.execute(
                command.format(table=connect_db.get_table(db_object), name=subname)
            )
        except:
            return (
                "Unfortunately, we do not have deal data available on "
                + subname.replace("-", " ")
                + f" sub at this time."
            )

        # Fetches us all the rows so we can grab data from each
        records = cur.fetchall()
        for row in records:
            last_on_sale = row[1]
            on_sale = row[2]
            price = row[3]
            image = row[4]
        # Creates a dictionary
        data = {}

        # Creates a primary catagory
        data["sub_names"] = []

        # Create a default JSON structure
        data["sub_names"].append(
            {
                "sub_name": subname.lower(),
                "last_sale": last_on_sale,
                "status": on_sale,
                "price": price,
                "image": image,
            }
        )

        sub_info = json.dumps(data["sub_names"], indent=2)
        return sub_info
    except:
        return abort(404)
