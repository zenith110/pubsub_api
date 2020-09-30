import psycopg2
import json
import pandas as pd
import os
import requests
from PySide2 import QtWidgets, QtCore, QtGui
from ui import uploader
with open("settings/dblogin.json") as loop:
    data = json.load(loop)
class uploader(uploader.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(uploader, self).__init__()
        self.setupUi(self)
        self.upload.clicked.connect(self.add_entry)
        self.delete_2.clicked.connect(self.delete_entry)
    def delete_entry(self):
        sub_name = self.sub_name.text()
        dates = self.date.text()
        on_sale = self.on_sale.text()
        sub_name = sub_name.replace(" ", "-").lower()
        price = self.price.text()
        image = self.image.text()
            
        #Establish a connection using the dblogin.json
        connection = psycopg2.connect(user = data["Login"]["Username"],
                                    password = data["Login"]["Password"],
                                    host = data["Login"]["Host"],
                                    port = data["Login"]["Port"],
                                    database = data["Login"]["Database"])
        cur = connection.cursor()
        print("Deleting!")
        cur.execute("DELETE FROM " + data["Login"]["Table"] + " WHERE pubsub_name LIKE '%" + sub_name + "%'")
        
        #Push the data onto the database
        connection.commit()
                
        print("Data now deleted, close if done!")
        #Close the database
        connection.close()
    def add_entry(self):
            sub_name = self.sub_name.text()
            dates = self.date.text()
            on_sale = self.on_sale.text()
            sub_name = sub_name.replace(" ", "-").lower()
            price = self.price.text()
            image = self.image.text()
            
            #Establish a connection using the dblogin.json
            connection = psycopg2.connect(user = data["Login"]["Username"],
                                    password = data["Login"]["Password"],
                                    host = data["Login"]["Host"],
                                    port = data["Login"]["Port"],
                                    database = data["Login"]["Database"])

            cur = connection.cursor()
            # Checks to see if that row exist
            # if(cur.execute("SELECT exists(select 1 from" + data["Login"]["Table"] + "where pubsub_name=%s"), (sub_name)):
            #     print("%s exist, let's update the data instead!", sub_name)
            #     cur.execute("Update %s set on_sale = %s where pubsub_name = %s", data["Login"]["Table"], on_sale, sub_name)
            # Inserts the data into each column
            cur.execute('INSERT INTO ' + data["Login"]["Table"] + '(pubsub_name, dates, on_sale, price, image) VALUES (%s, %s, %s, %s, %s)', (sub_name, dates, on_sale, price, image))
                
                
            #Push the data onto the database
            connection.commit()
                
            print("Data now pushed, close if done!")
            #Close the database
            connection.close()
                

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    qt_app = uploader()
    qt_app.show()
    app.exec_()