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
def delete_sub(sub_name):
    db_object = DatabaseObject()
    db_object.user = os.getenv("USERNAME_DB")
    db_object.password = os.getenv("PASSWORD")
    db_object.host = os.getenv("HOST")
    db_object.port = os.getenv("PORT")
    db_object.database = os.getenv("DATABASE")
    db_object.table = os.getenv("TABLE")
    connection = db_utils.connect(db_object)
    cur = connection.cursor()
    db_utils.remove_sub(cur, sub_name, db_utils.get_table(db_object), db_object, connection)
def update_sub(sub_name, dates):
    db_object = DatabaseObject()
    db_object.user = os.getenv("USERNAME_DB")
    db_object.password = os.getenv("PASSWORD")
    db_object.host = os.getenv("DBHOST")
    db_object.port = os.getenv("PORT")
    db_object.database = os.getenv("DATABASE")
    db_object.table = os.getenv("TABLE")
    print(db_object.password)
    connection = db_utils.connect(db_object)
    cur = connection.cursor()
    db_utils.update_sale_date(cur, sub_name, db_utils.get_table(db_object), db_object, connection, dates)
if __name__ == "__main__":
    sub_name = argv[2]
    operation = argv[1]
    if(operation == "delete"):
        delete_sub(sub_name)
    elif(operation == "update"):
        dates = argv[3]
        update_sub(sub_name, dates)