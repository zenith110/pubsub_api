from flask import Flask, render_template, request, redirect, jsonify
from flask.json import jsonify
import requests
import psycopg2
import json
import connect_db
app = Flask(__name__, static_url_path='/static')

@app.route("/allsubs/", methods =["POST", "GET"])
def all_names():

    connection = connectIt()   
    cur = connection.cursor()

    query = "SELECT pubsub_name FROM {table} ORDER BY pubsub"
    cur.execute(query.format(table = data["Login"]["Table"]))
    
    records = cur.fetchall()

    data = {}

    # Creates a primary catagory
    data["All_subs".lower()] = []

    # Create a default JSON structure
    for sub in records:
        records.
        data["All_subs".lower()].append(
        {
            {"name": sub} #this may need to be sub[0] not sure
        })
        
    return jsonify(data["All_subs".lower()])

@app.route("/subs/", methods =["POST", "GET"])    
def sub():
    if request.method == "GET":
            sub_name = request.args.get("name")
            if(sub_name == ""):
                sub = random_sub()
                return sub
            else:
                sub = sub_runner(sub_name)
                return sub

def random_sub():
    sub = connect_db.connect_random()     
    return sub
def sub_runner(subname):
    sub = connect_db.connect(subname)         
    return sub
                
               
@app.route("/", methods =["POST", "GET"])
def index():
        return render_template("index.html")
        
        
def connectIt():
    return psycopg2.connect(user = data["Login"]["Username"],
                                        password = data["Login"]["Password"],
                                        host = data["Login"]["Host"],
                                        port = data["Login"]["Port"],
                                        database = data["Login"]["Database"]) 

    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)