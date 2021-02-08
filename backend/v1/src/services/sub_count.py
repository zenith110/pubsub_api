import connect_db
from flask import Flask, render_template, request, redirect, jsonify, abort


def count():
    connection = connect_db.connect()
    cur = connection.cursor()
    query = "SELECT COUNT(*) FROM {table} where pubsub_name is NOT NULL"
    cur.execute(query.format(table=connect_db.get_table()))
    count = cur.fetchone()
    count = str(count)
    # Remove the tuple aspect of the number
    count = count.replace("(", "").replace(",", "").replace(")", "")

    return count
