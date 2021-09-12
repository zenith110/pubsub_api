import psycopg2
import json

"""
Allows us to query specific commands
"""


def close(connection):
    # Push the data onto the database
    connection.commit()

    print("Closing connection to the database!")
    # Close the database
    connection.close()


def get_table(db_object):
    return db_object.table


def connect(db_object):
    print(vars(db_object))
    return psycopg2.connect(
        user=db_object.user,
        password=db_object.password,
        host=db_object.host,
        port=db_object.port,
        database=db_object.database,
    )
