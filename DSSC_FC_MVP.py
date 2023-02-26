from config import config_global
from DSSC_FC_MVP_data_collect import download
#import DSSC_FC_MVP_storage as st
from DSSC_FC_MVP_storage import mongo
from DSSC_FC_MVP_StatisticalAnalysis import Stats
from DSSC_FC_MVP_Visualization import visualization
import extract_mongo
import json
import pandas as pd
import pymongo



dc = download(config_global.tickers)
dc.data_collect()

data = mongo(config_global.data)
data.store_mongo()
extract_mongo.extract_mongo()

st = Stats(config_global.data_ext)
st.calculate_stats()

V = visualization(config_global.data_ext)
V.volume_plot()
V.close_plot()