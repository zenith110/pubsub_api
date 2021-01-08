import connect_db
from flask import Flask, render_template, jsonify


def all_subs_data():
    connection = connect_db.connect()
    cur = connection.cursor()

    query = "SELECT pubsub_name FROM {table} ORDER BY on_sale"
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

    return jsonify(data["All_subs".lower()])
