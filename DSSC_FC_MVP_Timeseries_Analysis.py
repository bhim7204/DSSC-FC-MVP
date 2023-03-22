import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pylab import rcParams
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import TimeSeriesSplit
import numpy as np



class timeseries_analysis:
    
    def timeseries_train_test_split(self,X, y, test_size):
        '''
            Perform train-test split with respect to time series structure
        '''
        # get the index after which test set starts
        test_index = int(len(X)*(1-test_size)) 
        X_train = X.iloc[:test_index]
        y_train = y.iloc[:test_index]
        X_test = X.iloc[test_index:]
        y_test = y.iloc[test_index:]
        return X_train, X_test, y_train, y_test
    
    def mean_absolute_percentage_error(self, y_true, y_pred): 
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    

    def plotModelResults(self, model, X_train, X_test, y_test, y_train, plot_intervals=False, plot_anomalies=False):
        """
            Plots modelled vs fact values, prediction intervals and anomalies
        
        """
        # for time-series cross-validation set 5 folds 
        tscv = TimeSeriesSplit(n_splits=5)

        prediction = model.predict(X_test)
        plt.figure(figsize=(15, 7))
        plt.plot(prediction, "g", label="prediction", linewidth=2.0)
        plt.plot(y_test.values, label="actual", linewidth=2.0)
        
        if plot_intervals:
            cv = cross_val_score(model, X_train, y_train, 
                                        cv=tscv, 
                                        scoring="neg_mean_absolute_error")
            mae = cv.mean() * (-1)
            deviation = cv.std()
            
            scale = 1.96
            lower = prediction - (mae + scale * deviation)
            upper = prediction + (mae + scale * deviation)
            
            plt.plot(lower, "r--", label="upper bond / lower bond", alpha=0.5)
            plt.plot(upper, "r--", alpha=0.5)
            
            if plot_anomalies:
                anomalies = np.array([np.NaN]*len(y_test))
                anomalies[y_test<lower] = y_test[y_test<lower]
                anomalies[y_test>upper] = y_test[y_test>upper]
                plt.plot(anomalies, "o", markersize=10, label = "Anomalies")
        
        error = self.mean_absolute_percentage_error(prediction, y_test)
        plt.title("Regression plot for High price for IBM with Mean absolute percentage error {0:.2f}%".format(error))
        plt.xlabel('time')
        plt.ylabel('High price')
        plt.legend(loc="best")
        plt.tight_layout()
        plt.grid(True)
        plt.show()
    

    
    def analysis(self, df):
        # plotting percentage change
        df['Change'] = df.High.div(df.High.shift())
        df['Return'] = df.Change.sub(1).mul(100)
        df['Return'].plot(figsize=(20,8),xlabel= 'Time', ylabel='High price',title='Percentage change for IBM')

        #absolute change in successive rows
        df.High.diff().plot(figsize=(20,6),xlabel= 'Time', ylabel='High price',title='Daily change in IBM High price')

        # Now, for decomposition...
        rcParams['figure.figsize'] = 11, 9
        decomposed_data_volume = sm.tsa.seasonal_decompose(df.High,period = 7) # The frequncy is weekly
        decomposed_data_volume.plot()
        plt.show()

        # Candlestick chart of IBM
        fig = go.Figure(data=[go.Candlestick(x= df.index,
                        open=df.Open,
                        high=df.High,
                        low=df.Low,
                        close=df.Close)])

        fig.show()

        # Creating a copy of the initial datagrame to make various transformations 
        # we are only copying the Date and closing price
        df2= df[['Date','High']].copy()
        df2.rename(columns = {'High':'y'},inplace = True)
        df2.set_index('Date',inplace = True)

        '''
        here we are performing linear regression in the data so here we are creating
        feature set which will be the past data so we are Adding the lag of the target variable from 6 steps back up to 19
        '''
        for i in range(6, 20):
            df2["lag_{}".format(i)] = df2.y.shift(i)

        y = df2.dropna().y
        X = df2.dropna().drop(['y'], axis=1)

        # reserve 30% of data for testing
        X_train, X_test, y_train, y_test = self.timeseries_train_test_split(X, y, test_size=0.3)

        # machine learning in two lines
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        self.plotModelResults(lr,X_train, X_test, y_test, y_train, plot_intervals=True)

# read the csv file
df = pd.read_csv('all_stocks.csv')
# the date column is in object type so we need to change it into datetime format
df['Date'] = pd.to_datetime(df.Date,errors='ignore')
df['Date'] = df['Date'].apply(lambda x : x.strftime('%Y-%m-%d'))
df['Date'] = pd.to_datetime(df.Date,errors='ignore')
out = timeseries_analysis()
out.analysis(df)
   