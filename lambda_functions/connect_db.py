import psycopg2
import json
from decouple import config

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
    return config("TABLE")


def connect():
    return psycopg2.connect(
        user=config("USERNAME"),
        password=config("PASSWORD"),
        host=config("HOST"),
        port=config("PORT"),
        database=config("DATABASE"),
    )
