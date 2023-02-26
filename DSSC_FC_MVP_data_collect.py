import yfinance as yf
from config import config_global
import pandas as pd

class download:
    def __init__(self,tickers):
                self.tickers = tickers

    def data_collect(self):
        """
        Downloads data with yfinance for all stocks .
        This function is shared in main function.
        """
        
        #download the data for the given date range
        config_global.data = yf.download(self.tickers, start = '2021-1-3', end = '2021-12-31', group_by='tickers')

        # save the data in csv format
        config_global.data.to_csv('all_stocks.csv')