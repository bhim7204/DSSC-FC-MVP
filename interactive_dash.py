import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Load the data from a CSV file
df = pd.read_csv('all_stocks.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the options for the dropdown menu
options = [
    {'label': 'Open Price Plot', 'value': 'open'},
    {'label': 'Close Price Plot', 'value': 'close'},
    {'label': 'High Price Plot', 'value': 'high'},
    {'label': 'Low Price Plot', 'value': 'low'},
    {'label': 'Adjusted Close Price Plot', 'value': 'adj'},
    {'label': 'Volume Plot', 'value': 'volume'}
]

# Define the layout of the Dash app
app.layout = html.Div(children=[
    html.H1(children='Plotly Graphs For IBM'),

    # Create the dropdown menu
    dcc.Dropdown(
        id='graph-dropdown',
        options=options,
        value='line'
    ),

    # Create the graph based on the dropdown selection
    dcc.Graph(id='graph')
])

# Define the callback to update the graph based on the dropdown selection
@app.callback(
    Output('graph', 'figure'),
    [Input('graph-dropdown', 'value')]
)
def update_graph(selected_value):
    if selected_value == 'close':
        fig = px.line(df, x='Date', y='Close', title='Closing Price')
    elif selected_value == 'open':
        fig = px.line(df, x='Date', y='Open', title='Opening Price')
    elif selected_value == 'high':
        fig = px.line(df, x='Date', y='High', title='High Price')
    elif selected_value == 'low':
        fig = px.line(df, x='Date', y='Low', title='Low Price')
    elif selected_value == 'adj':
        fig = px.line(df, x='Date', y='Adj Close', title='Adjusted Closing Price')
    elif selected_value == 'volume':
        fig = px.line(df, x='Date', y='Volume', title='Volume of Transaction')
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server()
