import sqlite3
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import plotly
import plotly.graph_objs as go
import pandas as pd


def run_query_withparms(sql):
    conn = sqlite3.connect('serp_data.db')
    df = pd.read_sql_query(sql , conn)
  #  print(df)
    return df

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Label("Text Input"),
    dcc.Input(id='text_in',value="MTL",type="text"),
    html.Div(id='tab_container',children=[html.Div(dt.DataTable(id="tab_out"))])
    ])


@app.callback(Output("tab_container","children"), [Input("text_in","value")])

def run_query(value):
    sql2 = 'SELECT * FROM queries limit 10;'
    return [html.Div([dt.DataTable(data=run_query_withparms(sql2))])]

if __name__ == '__main__':
    app.run_server(debug=True)

