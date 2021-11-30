import connect_db
from flask import Flask, jsonify


def all_subs_data():
    connection = connect_db.connect()
    cur = connection.cursor()

    query = (
        "SELECT pubsub_name FROM {table} WHERE pubsub_name is not NULL ORDER BY on_sale"
    )
    cur.execute(query.format(table=connect_db.get_table()))

    records = cur.fetchall()

    data = {}

    """
    Creates a primary catagory
    """
    data["All_subs".lower()] = []

    """
    Create a default JSON structure
    """
    for sub in records:
        data["All_subs".lower()].append({"name": sub[0]})
    response = jsonify(data["All_subs".lower()])
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
