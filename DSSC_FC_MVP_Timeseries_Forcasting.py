# import all the required libraries

from prophet import Prophet
import matplotlib.pyplot as plt
import pandas as pd
from prophet.plot import add_changepoints_to_plot



class prophet_viz:
    def __init__(self,df,period):
        self.df = df
        self.period = period
        
    def prediction(self):
        # changing Date to ds and target variable open price to y

        df2 = self.df.rename(columns={'Date': 'ds',
                        'Close': 'y'})

        # set the uncertainty interval to 95% 
        my_model = Prophet(interval_width=0.95, changepoint_range= 1)
        my_model.fit(df2)

        # creating future dates for forcasting
        future_dates = my_model.make_future_dataframe(periods=36, freq='D')

        '''
        here yhat is the predicted variable whereas yhat_lower is lower bound of the forcast
        yhat_upper is upper bound of the forcast
        '''
        forecast = my_model.predict(future_dates)
        print(forecast.tail())

        # plotting the line graph of the data
        ax = df2.set_index('ds').plot(figsize=(12, 8))
        ax.set_ylabel('closing price of IBM')
        ax.set_xlabel('Date')

        # plotting the forcast along with the uncertainity level
        my_model.plot(forecast, uncertainty=True)

        # plotting the trend and seasonality of the data
        my_model.plot_components(forecast)
        
        # plotting points where abrupt changes have occur
        fig = my_model.plot(forecast)
        add_changepoints_to_plot(fig.gca(), my_model, forecast)
        plt.show()

        # places where changepoints occur
        print("Times where abrupt changes occured:\n", my_model.changepoints)

# read the csv file
df = pd.read_csv('all_stocks.csv')

# Creating a copy of the initial datagrame to make various transformations 
# we are only copying the Date and closing price
df2= df[['Date','Close']].copy()

# the date column is in object type so we need to change it into datetime format
df2['Date'] = pd.to_datetime(df2.Date,errors='ignore')
df2['Date'] = df2['Date'].apply(lambda x : x.strftime('%Y-%m-%d'))
df2['Date'] = pd.to_datetime(df2.Date,errors='ignore')

predict = prophet_viz(df2,30)
predict.prediction()