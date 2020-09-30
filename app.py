from flask import Flask, render_template, request, redirect
from flask.json import jsonify
import requests
import psycopg2
import json
import connect_db
app = Flask(__name__, static_url_path='/static')
@app.route("/allsubs/", methods =["POST", "GET"])
def all_names():
     # Creates a dictionary
    data = {}

    # Creates a primary catagory
    data["All_subs".lower()] = []

    # Create a default JSON structure
    data["All_subs".lower()].append(
    {
        {"sub_name": "boar-head-jerk-turkey"},
        {"sub_name_2": "chicken-tenders"}
    })

    sub_info = json.dumps(data, indent = 2)
        
    return sub_info
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
        
        
    

    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)