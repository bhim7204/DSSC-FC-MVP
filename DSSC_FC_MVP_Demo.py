import pandas as pd
import holoviews as hv
import hvplot.pandas
import panel as pn
from pylab import *
import plotly.graph_objects as go

hv.extension('bokeh')
pn.extension()



class demo:
    def demo_plot(self,df):
        # Define the items to be displayed in the drop-down menu
        menu_items = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]

        # Create the drop-down menu widget
        dropdown = pn.widgets.Select(options=menu_items)

        @pn.depends(dropdown)
        def ticker(dropdown):
            return '### {} Price of IBM'.format(dropdown)
        
        @pn.depends(dropdown)
        def plot_line(dropdown):
            return df.hvplot.line(x = 'Date',y = f"{dropdown}", title = f"{dropdown}  of IBM")
        
        # Candlestick chart of IBM
        def candle():
            fig = go.Figure(data=[go.Candlestick(x= df.index,
                                open=df.Open,
                                high=df.High,
                                low=df.Low,
                                close=df.Close)])
            return fig.show()
        
        plots_box = pn.WidgetBox(pn.Column(pn.Row(ticker, dropdown)
                                   ,pn.Row(pn.bind(plot_line,dropdown)),
                                   #pn.Row(pn.bind(candle)), 
                                     align="start",
                                   sizing_mode="stretch_width"))

        dashboard = pn.Row(plots_box, sizing_mode="stretch_width")
        dashboard.show()

df = pd.read_csv('all_stocks.csv')

# the date column is in object type so we need to change it into datetime format
df['Date'] = pd.to_datetime(df.Date,errors='ignore')
df['Date'] = df['Date'].apply(lambda x : x.strftime('%Y-%m-%d'))
df['Date'] = pd.to_datetime(df.Date,errors='ignore')

demo1 = demo()
demo1.demo_plot(df)
