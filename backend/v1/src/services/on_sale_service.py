import psycopg2
import json
import connect_db
from flask import Flask, render_template, jsonify


def on_sale_check():
    connection = connect_db.connect()
    cur = connection.cursor()
    """
    Queries if there are no none entires
    """
    query = "SELECT pubsub_name, dates, on_sale, price, image FROM {table} where pubsub_name is NOT NULL"
    cur.execute(query.format(table=connect_db.get_table()))
    sub_name = []
    last_on_sale = []
    on_sale = []
    price = []
    image = []

    records = cur.fetchall()
    """
    Loops through all the columns and rows
    """
    for i in range(len(records)):
        sub_name.append(records[i][0])
        last_on_sale.append(records[i][1])
        on_sale.append(records[i][2])
        price.append(records[i][3])
        image.append(records[i][4])
    sub_name = [x for x in sub_name if x is not None]
    original_name = [w.replace("-", " ") for w in sub_name]
    data = {}

    """
    Creates a primary catagory
    """
    data["All_subs".lower()] = []

    """
    Create a default JSON structure
    """
    for i in range(len(records)):
        data["All_subs".lower()].append(
            {
                "name": original_name[i],
                "on_sale": on_sale[i],
                "image": image[i],
                "last_on_sale": last_on_sale[i],
                "price": price[i],
                "query_name": sub_name[i],
            }
        )
    response = jsonify(data["All_subs".lower()])
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
