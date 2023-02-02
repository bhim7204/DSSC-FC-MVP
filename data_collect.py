import yfinance as yf
import pandas as pd


tickers = ['IBM','MSFT','AAPL']
data = yf.download(tickers, start = '2021-1-3', end = '2021-12-31', group_by='ticker')
data.to_csv('all_stocks.csv')