import pandas as pd
import pymongo 
from config import config_global
import json 

def extract_mongo():

            # load the credentials from the JSON file
            with open("DSSC-FC-MVP-Configuration.json", "r") as file:
                credentials = json.load(file)

            # extract the username and password from the credentials
            username = credentials["username"]
            password = credentials["password"]


            myclient = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@cluster0.zwmtp4o.mongodb.net/?retryWrites=true&w=majority")
            mydb = myclient["stock_data"]
            mycol = mydb["first_trail"]
            
            documents = mycol.find()
            #myclient.close()
            config_global.data_ext = pd.DataFrame(documents)
            config_global.data_ext.drop(columns=['_id'], inplace= True)
            #print(config_global.data_ext)