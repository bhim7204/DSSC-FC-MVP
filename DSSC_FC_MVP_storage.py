import pymongo
from config import config_global
import json
import sys
import pandas as pd
#mongodb://localhost:27017/

class mongo:
    def __init__(self,df):
            self.df = df

    def store_mongo(self):

        # load the credentials from the JSON file
        with open("DSSC-FC-MVP-Configuration.json", "r") as file:
            credentials = json.load(file)

        # extract the username and password from the credentials
        username = credentials["username"]
        password = credentials["password"]


        myclient = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@cluster0.zwmtp4o.mongodb.net/?retryWrites=true&w=majority")
        mydb = myclient["stock_data"]
        mycol = mydb["first_trail"]
        records = self.df.to_dict(orient='records')
        mycol.insert_many(records)

        #mycol.insert_many([records])
        #myclient.close()

   
            