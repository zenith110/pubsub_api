import psycopg2
import json
import os

"""
Allows us to query specific commands
"""


def close(connection):
    # Push the data onto the database
    connection.commit()

    print("Closing connection to the database!")
    # Close the database
    connection.close()


def get_table():
    return os.environ.get("Table")


def connect():
    return psycopg2.connect(
        user=os.environ.get("Username"),
        password=os.environ.get("Password"),
        host=os.environ.get("Host"),
        port=os.environ.get("Port"),
        database=os.environ.get("Database"),
    )
