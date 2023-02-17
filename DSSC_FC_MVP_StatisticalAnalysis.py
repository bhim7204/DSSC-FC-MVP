import pandas as pd
import numpy as np
from config import config_global

class Stats:
    def __init__(self,df):
        self.df = df
    def calculate_stats(df):
        stats = {}
        for tickers in config_global.tickers:
            stats[tickers,'Minimum Close'] = df[tickers,'Close'].min()
            stats[tickers,'Maximum Close'] = df[tickers,'Close'].max()
            stats[tickers,'Range Close'] = stats[tickers,'Maximum Close'] - stats[tickers,'Minimum Close']
            stats[tickers,'Median'] = df[tickers,'Close'].median()
            stats[tickers,'Mean'] = df[tickers,'Close'].mean()
            stats[tickers,'Variance'] = df[tickers,'Close'].var()
            stats[tickers,'Standard deviation'] = df[tickers,'Close'].std()
        config_global.Statistics = pd.DataFrame(stats)
        config_global.Statistics.to_csv('all_stats.csv')
