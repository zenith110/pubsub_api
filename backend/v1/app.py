from flask import Flask, render_template, request, redirect, jsonify, abort
from flask.json import jsonify
import requests
import psycopg2
import json
import connect_db
from flask_cors import CORS
from services import mailchimp
import re
app = Flask(__name__, static_url_path='/static')
CORS(app)
# Route to add phone numbers
@app.route("/phone/", methods = ["POST", "GET"])
def phone_add():
    content = request.json
    phone_number = content["phoneNumber"]
    # Loops through the entire string character by character, and only grabs the numbers
    # # Ignores the numbers or special characters
    getVals = list([val for val in phone_number if val.isnumeric()]) 
    # Joins back the list into a string to print at the end 
    phone_number = "".join(getVals)
    connection = connect_db.connect()   
    cur = connection.cursor()
    # Checks to see if that row exist
    exist_query = "select exists(select 1 from {table} where phone_number ='{phone}' limit 1)"
    exist_check = cur.execute(exist_query.format(table = connect_db.get_table(), phone = phone_number))
    count = cur.fetchone()[0]
    if(count == True):
        print("Phone number within database, skipping!")
    else:
        print("Inserting " + phone_number + " into the db!")
        cur.execute('INSERT INTO ' + connect_db.get_table() + '(phone_number) VALUES (' + phone_number + ')')
        connect_db.close(connection)
    return "Phone data now complete!"
    
# Gets the current sub count
@app.route("/totalcount/", methods = ["POST", "GET"])
def num():
    connection = connect_db.connect()   
    cur = connection.cursor()
    query = "SELECT COUNT(*) FROM {table} where pubsub_name is NOT NULL"
    cur.execute(query.format(table = connect_db.get_table()))
    count = cur.fetchone()
    count = str(count)
    # Remove the tuple aspect of the number
    count = count.replace("(", "").replace(",", "").replace(")", "")
    return count

@app.route("/email/", methods=["POST"])
def email():
    content = request.json
    
    # Parses the JSON data to be dumped into a mailchimp list
    email = content["email"]
    first_name = content["name"]

    # Sends off data to add to list
    mailchimp.register_data(email, first_name)


@app.route("/onsale/", methods = ["POST", "GET"])
def onsale_data():
    connection = connect_db.connect()   
    cur = connection.cursor()
    query = "SELECT pubsub_name, dates, on_sale, price, image FROM {table} where pubsub_name is NOT NULL"
    cur.execute(query.format(table = connect_db.get_table()))
    sub_name = []
    last_on_sale = []
    on_sale = []
    price = []
    image = []
    records = cur.fetchall()
    for i in range(len(records)):
        sub_name.append(records[i][0])
        last_on_sale.append(records[i][1])
        on_sale.append(records[i][2])
        price.append(records[i][3])
        image.append(records[i][4])
    sub_name = [x for x in sub_name if x is not None]
    data = {}
    
    # Creates a primary catagory
    data["All_subs".lower()] = []

    # Create a default JSON structure
    for i in range(len(records)):
        data["All_subs".lower()].append({
            "name": sub_name[i],
            "on_sale": on_sale[i],
            "image": image[i],
            "last_on_sale": last_on_sale[i],
            "price": price[i]
            }) 
        
    return jsonify(data["All_subs".lower()])
@app.route("/allsubs/", methods =["POST", "GET"])
def all_names():

    connection = connect_db.connect()   
    cur = connection.cursor()

    query = "SELECT pubsub_name FROM {table} ORDER BY on_sale"
    cur.execute(query.format(table = connect_db.get_table()))
    
    records = cur.fetchall()

    data = {}

    # Creates a primary catagory
    data["All_subs".lower()] = []

    # Create a default JSON structure
    for sub in records:
        data["All_subs".lower()].append({"name": sub[0]}) 
        
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
    try:
        connection = connect_db.connect()
        cur = connection.cursor()
        # Checks to see if the name exist in the record, then grabs a random row from that column limiting it to one.
        command = "SELECT * FROM {table} ORDER BY random()"
        query = cur.execute(command.format(table = connect_db.get_table()))
        
        # Fetches us all the rows so we can grab data from each
        records = cur.fetchall()
        for row in records:
            subname = row[0]
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
                    
                    
        sub_info = json.dumps(data[subname.lower()], indent = 2)
        return sub_info
    except:
        return abort(404)

def sub_runner(subname):
    try:
        connection = connect_db.connect()
        cur = connection.cursor()
        # Checks to see if the name exist in the record, then grabs a random row from that column limiting it to one.
        try:
            command = "SELECT * FROM {table} WHERE pubsub_name = '{name}' ORDER BY dates DESC LIMIT 1"
            query = cur.execute(command.format(table = connect_db.get_table(), name = subname))
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
                        
        sub_info = json.dumps(data[subname.lower()], indent = 2)
        return sub_info
    except:
        return abort(404)
                
               
@app.route("/", methods =["POST", "GET"])
def index():
        return render_template("index.html")
        
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)