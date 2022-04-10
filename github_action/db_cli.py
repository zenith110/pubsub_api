import db_utils
import os
from sys import argv
from dotenv import load_dotenv
from os.path import join, dirname


class DatabaseObject:
    def __init__(self) -> None:
        self.user = ""
        self.password = ""
        self.host = ""
        self.port = ""
        self.database = ""
        self.table = ""


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
db_object = DatabaseObject()
db_object.user = os.getenv("USERNAME_DB")
db_object.password = os.getenv("PASSWORD")
db_object.host = os.getenv("DBHOST")
db_object.port = os.getenv("PORT")
db_object.database = os.getenv("DATABASE")
db_object.table = os.getenv("TABLE")


def delete_sub(sub_name):
    connection = db_utils.connect(db_object)
    cur = connection.cursor()

    db_utils.remove_sub(
        cur, sub_name, db_utils.get_table(db_object), db_object, connection
    )


def update_sub(sub_name, dates):
    connection = db_utils.connect(db_object)
    cur = connection.cursor()
    db_utils.update_sale_date(
        cur, sub_name, db_utils.get_table(db_object), db_object, connection, dates
    )


def update_state(sub_name, state):
    connection = db_utils.connect(db_object)
    cur = connection.cursor()
    db_utils.update_state(
        cur, sub_name, db_utils.get_table(db_object), db_object, connection, state
    )


if __name__ == "__main__":
    operation = argv[1]
    sub_name = argv[2]
    if operation == "delete":
        delete_sub(sub_name)
    elif operation == "update":
        dates = argv[3]
        update_sub(sub_name, dates)
    elif operation == "state":
        state = argv[3]
        update_state(sub_name, state)
