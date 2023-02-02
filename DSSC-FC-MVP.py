import yfinance as yf
import pandas as pd


def compute(ticker):
    """
    Downloads data with yfinance for all stocks and generates all parameters required by filters.
    This function is shared between the single and multiple stocks to reuse the existing variables.
    """
    
    print('\nRetrieving data...')
    # Download data for all symbols in the CSV
    data = yf.download('IBM', start=2019-1-1,
                           end=2020-1-1, group_by='ticker')

    # Remove all columns that has no data
    data.dropna(axis=1, inplace=True)