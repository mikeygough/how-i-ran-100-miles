# test dash dashboard
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)


# load in (numeric) data
df = pd.read_csv('data/numeric_data.csv', parse_dates=['Date'],
                         infer_datetime_format=True, index_col='Date',
                         thousands=',')

# create the fig
fig = px.line(data_frame=df, y='Distance')

total_ran = int(df['Distance'].sum())

# create layout
app.layout = html.Div(children=[
    
    html.H1(children='Run 100 Miles'),
    
    html.Div(id='total_distance', 
             children='{} Miles'.format(total_ran)),
    
    dcc.DatePickerRange(id='date_filter',
                        start_date=df.index.min(),
                        end_date=df.index.max(),
                        min_date_allowed=df.index.min(),
                        max_date_allowed=df.index.max()),

    html.Div(id='output-container-date-picker-range'),
    
    dcc.Graph(id='graph1',
              figure=fig)
    ])

@app.callback(
    Output('graph1', 'figure'),
    Input('date_filter', 'start_date'),
    Input('date_filter', 'end_date'))
def updateGraph(start_date, end_date):
    if not start_date or not end_date:
        raise dash.exceptions.PreventUpdate
    else:
        return px.line(data_frame=df[start_date:end_date], y='Distance')

@app.callback(
    Output('total_distance', 'children'),
    Input('date_filter', 'start_date'),
    Input('date_filter', 'end_date'))
def updateTotalDistance(start_date, end_date):
    if not start_date or not end_date:
        raise dash.exceptions.PreventUpdate
    else:
        return '{} Miles'.format(int(df[start_date:end_date]['Distance'].sum()))

if __name__ == '__main__':
    app.run_server(debug=True)