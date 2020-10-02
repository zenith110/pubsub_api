import psycopg2
import json
"""
Allows us to query specific commands
"""
def get_table():
    with open("settings/dblogin.json", "r") as loop:
                        data = json.load(loop)
                        
    return data["Login"]["Table"]
def query_call(cur, query):
    with open("settings/dblogin.json", "r") as loop:
                        data = json.load(loop)
    cur.execute(query)
    
def connect():
    with open("settings/dblogin.json", "r") as loop:
                        data = json.load(loop)
    return psycopg2.connect(user = data["Login"]["Username"],
                                        password = data["Login"]["Password"],
                                        host = data["Login"]["Host"],
                                        port = data["Login"]["Port"],
                                        database = data["Login"]["Database"])    

        