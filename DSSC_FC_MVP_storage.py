import pymongo
from config import config_global
import json
import sys
#mongodb://localhost:27017/


def store_mongo(df):

    # load the credentials from the JSON file
    with open("DSSC-FC-MVP-Configuration.json", "r") as file:
        credentials = json.load(file)

    # extract the username and password from the credentials
    username = credentials["username"]
    password = credentials["password"]


    myclient = pymongo.MongoClient(f"mongodb://{username}:{password}@docdb-2023-02-10-13-57-31.cii0u59nxhlc.us-east-2.docdb.amazonaws.com:27017/?ssl=true&ssl_ca_certs=rds-combined-ca-bundle.pem&retryWrites=false")
    mydb = myclient["stock_data"]
    mycol = mydb["first_trail"]
    records = {'IBM':None,'MSFT':None}
    
    for tk in config_global.tickers:
        inf = []
        for i in range(df.shape[0]):
            inf.append(df[tk].iloc[i].tolist())
        records[tk] = inf   
       
    mycol.insert_many([records])
   # myclient.close()
