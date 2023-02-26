import pandas as pd
import numpy as np
import pymongo
import json
from config import config_global

class Stats:
    def __init__(self,df):
        self.df = df
        
    def calculate_stats(self):
        stats = {}
        
        stats['Minimum'] = self.df.min()
        stats['Maximum'] = self.df.max()
        stats['Range'] = stats['Maximum'] - stats['Minimum']
        stats['Median'] = self.df.median()
        stats['Mean'] = self.df.mean()
        stats['Variance'] = self.df.var()
        stats['Standard deviation'] = self.df.std()
    
        config_global.Statistics = pd.DataFrame(stats)
        config_global.Statistics.to_csv('all_stats.csv')
        #print(config_global.Statistics)
