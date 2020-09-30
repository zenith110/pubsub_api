from flask import Flask, render_template, request, redirect, jsonify
from flask.json import jsonify
import requests
import psycopg2
import json

app = Flask(__name__, static_url_path='/static')

@app.route("/allsubs/", methods =["POST", "GET"])
def all_names():

    connection = connectIt()   
    cur = connection.cursor()
    records = cur.fetchall()

    data = {}

    # Creates a primary catagory
    data["All_subs".lower()] = []

    # Create a default JSON structure
    for sub in records:
        records.
        data["All_subs".lower()].append(
        {
            {"name": sub}
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
    with open("settings/dblogin.json", "r") as loop:
                    data = json.load(loop)

    # Establish a connection using the dblogin.json
    connection = connectIt()
    cur = connection.cursor()
    command = "SELECT * from {table} ORDER BY random()"
    query = cur.execute(command.format(table = data["Login"]["Table"]))
     # Fetches us all the rows so we can grab data from each
    records = cur.fetchall()
    for row in records:
        sub_name = row[0]
        last_on_sale = row[1]
        on_sale = row[2]
        price = row[3]
        image = row[4]
                    
    # Creates a dictionary
    data = {}

    # Creates a primary catagory
    data[sub_name.lower()] = []

    # Create a default JSON structure
    data[sub_name.lower()].append(
    {
        "sub_name": sub_name.lower(),
        "last_sale": last_on_sale,
        "status": on_sale,
        "price": price,
        "image": image
    })
        
    return jsonify(sub_info)


def sub_runner(subname):
    with open("settings/dblogin.json", "r") as loop:
                    data = json.load(loop)
    #Establish a connection using the dblogin.json
    connection = connectIt()   
    cur = connection.cursor()
    # Checks to see if the name exist in the record, then grabs a random row from that column limiting it to one.
    try:
        command = "SELECT * FROM {table} WHERE pubsub_name = '{name}' ORDER BY dates DESC LIMIT 1"
        query = cur.execute(command.format(table = data["Login"]["Table"], name = subname))
    except:
        return "Unfortunately, we do not have deal data available on " + subname.replace("-", " ") + " sub at this time.\nOur current offers is the boar-head-jerk-turkey-and-gouda sub"
    
    # Fetches us all the rows so we can grab data from each
    records = cur.fetchall()
    for row in records:
        last_on_sale = row[1]
        on_sale = row[2]
        price = row[3]
        image = row[4]
                    
    # Creates a dictionary
    data = {}

    # Creates a primary catagory
    data[subname.lower()] = []

    # Create a default JSON structure
    data[subname.lower()].append(
    {
        "sub_name": subname.lower(),
        "last_sale": last_on_sale,
        "status": on_sale,
        "price": price,
        "image": image
    })
                
                
    sub_info = json.dumps(data, indent = 2)
        
    return sub_info
                
               
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