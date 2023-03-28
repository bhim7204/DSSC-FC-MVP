import pandas as pd
import holoviews as hv
from datetime import timedelta
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
        dropdown = pn.widgets.Select(name = '### Select a feature from below',options=menu_items)

        #radio buttons for line or bar plot
        radio_group = pn.widgets.RadioButtonGroup(
            name='Radio Button Group', options=['Line Plot', 'Bar Plot'], button_type='success')
        
        # Define the drop-down menu for tickers
        items = ['IBM','AAPL','TSLA','MSFT']
        # Create the drop-down menu widget
        tickers = pn.widgets.Select(name='Select a ticker from below', options=items, size=2)


        def intro():
            return f"""  This dashboard gives the **line, bar and candle stick plot** for the feature you select for the 
            selected Ticker """
        
        @pn.depends(dropdown, radio_group)
        def plot_line(dropdown,radio_group):
            if radio_group == 'Line Plot':
                pt = df.hvplot.line(x = 'Date',y = f"{dropdown}", title = f"{dropdown}  of IBM")
            else:
                pt = df.hvplot.bar(x = 'Date',y = f"{dropdown}",  title = f"{dropdown}  of IBM")
            return pt
        
        # Candlestick chart of IBM
        def _transform_data(raw_data: pd.DataFrame):
            data = raw_data[["Date", "Open", "High", "Low", "Close", "Volume"]].copy(deep=True).rename(columns={
                "Date": "time",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            })
            t_delta = timedelta(hours=1)
            data['time_start'] = data.time - 9*t_delta # rectangles start
            data['time_end'] = data.time + 9*t_delta    # rectangles end
            data['positive'] = ((data.close - data.open)>0).astype(int)
            return data
        
        def make_candle_stick(data):
            _delta = np.median(np.diff(data.time))
            candlestick = hv.Segments(data, kdims=['time', 'low', 'time', 'high']) * hv.Rectangles(data, kdims=['time_start','open', 'time_end', 'close'], vdims=['positive'])
            candlestick = candlestick.redim.label(Low='Values')
            return candlestick.opts(hv.opts.Rectangles(color='positive', cmap=['red', 'green'], title = 'Candle Stick plot of the Stock',responsive=True), hv.opts.Segments(color='black', height=400, responsive=True))

        data = _transform_data(raw_data= df)
        candle_stick_plot = make_candle_stick(data)
        


        plots_box = pn.WidgetBox(pn.Row(
                                    pn.Column(pn.pane.PNG('logo.png', height=350, width = 350), intro, dropdown, radio_group)
                                   ,pn.Column(pn.bind(plot_line,dropdown, radio_group),pn.pane.HoloViews(candle_stick_plot)),
                                   #pn.Row(pn.bind(candle)), 
                                     align="start",
                                   sizing_mode="stretch_width"))

        dashboard = pn.Row(plots_box, sizing_mode="stretch_width")
        dashboard.show()

df = pd.read_csv('all_stocks22.csv')

# the date column is in object type so we need to change it into datetime format
df['Date'] = pd.to_datetime(df.Date,errors='ignore')
df['Date'] = df['Date'].apply(lambda x : x.strftime('%Y-%m-%d'))
df['Date'] = pd.to_datetime(df.Date,errors='ignore')

demo1 = demo()
demo1.demo_plot(df)
