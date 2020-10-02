import psycopg2
import json
"""
Allows us to query specific commands
"""
def close(connection):
    #Push the data onto the database
    connection.commit()
                
    print("Data now deleted, close if done!")
    # Close the database
    connection.close()
def get_table():
    with open("settings/dblogin.json", "r") as loop:
                        data = json.load(loop)
                        
    return data["Login"]["Table"]

    
def connect():
    with open("settings/dblogin.json", "r") as loop:
                        data = json.load(loop)
    return psycopg2.connect(user = data["Login"]["Username"],
                                        password = data["Login"]["Password"],
                                        host = data["Login"]["Host"],
                                        port = data["Login"]["Port"],
                                        database = data["Login"]["Database"])    

        