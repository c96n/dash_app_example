#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

#preprocessing
df = pd.read_csv("nama_10_gdp_1_Data.csv")

available_indicators = df['NA_ITEM'].unique()
available_indicators = np.sort(available_indicators)
available_units = df['UNIT'].unique()
available_units = np.sort(available_units)
available_countries = df['GEO'].unique()

#start building the app
app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

#header
app.layout = html.Div([  
    html.Div([
        html.H1(children="European GDP Data Dashboard",
               style={
                   'textAlign': 'center'
               })
    ]),
        
#first output layout
    
    #header Text first graph
    html.Div([
        html.H2(children="First Graph: Relation between two of the indicators",
                 style={
                   'textAlign': 'center'
               }),
    ]),
    
    #input indicator
    html.Div([
        html.H4(children="Please select the first indicator:",
                style={'textAlign': 'center'}
               ),
        html.Div([
            dcc.Dropdown(
                id="indicator_x1",
                options=[{'label': i, 'value': i} for i in available_indicators],
                value="Acquisitions less disposals of valuables",
            ),
            dcc.RadioItems(
                id='xaxis-type1',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            ), 
        ],
            style={'width': '100%', 'display': 'inline-block', 'textAlign': 'center'}),
    ]), 
    
    #input second indicator    
    html.Div([
        html.H4(children="Please select the second indicator:",
                style={
                'textAlign': 'center'
                }),
        html.Div([
            dcc.Dropdown(
                id="indicator_y1",
                options=[{'label': i, 'value': i} for i in available_indicators],
                value="Actual individual consumption"
            ),
            dcc.RadioItems(
                id='yaxis-type1',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
            style={'width': '100%', 'display': 'inline-block', 'textAlign': 'center'}),
    ]),
    
    #input unit   
    html.Div([
        html.H4(children="Please select the unit:",
                style={
                'textAlign': 'center'
                }),
        html.Div([
            dcc.Dropdown(
                id="unit_1",
                options=[{'label': i, 'value': i} for i in available_units],
                value="Chain linked volumes (2010), million euro"
            ),
        ],
            style={'width': '100%', 'display': 'inline-block', 'textAlign': 'center'}),
    ]),

    #year slider
    html.Div([
        html.H4(children="Please select the desired year:",
                style={
                    'textAlign': 'center'
                }),
            
        dcc.Slider(
            id='year--slider1',
            min=df['TIME'].min(),
            max=df['TIME'].max(),
            value=df['TIME'].max(),
            step=None,
            marks={str(year): str(year) for year in df['TIME'].unique()}),
    ]),
    
    #graph 1
    html.Div([
        dcc.Graph(id="indicator-graphic1"),
    ]),
    
    #border
    html.Div([
        html.Hr(),
    ]),
    
    
#second output layout
    
    #header Text second graph
    html.Div([
        html.H2(children="Second Graph: Historical Indicator performance per country",
                     style={
                       'textAlign': 'center'
                   }),
    ]),
    
    #input country
    html.Div([
        html.H4(children="Please select the country:",
                style={
                    'textAlign': 'center'
                }),
        html.Div([
            dcc.Dropdown(
                id="countries",
                options=[{'label': i, 'value': i} for i in available_countries],
                value="European Union - 28 countries"
            ),
        ],
            style={'width': '100%', 'display': 'inline-block', 'textAlign': 'center'}),
    ]),
    
    #input indicator
    html.Div([
        html.H4(children="Please select the indicator:",
                style={
                    'textAlign': 'center'
                }),
        html.Div([
            dcc.Dropdown(
                id="indicator_y2",
                options=[{'label': i, 'value': i} for i in available_indicators],
                value="Acquisitions less disposals of valuables"
            ),
            dcc.RadioItems(
                id='yaxis-type2',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
            style={'width': '100%', 'display': 'inline-block', 'textAlign': 'center'}),
    ]),
    #input unit   
    html.Div([
        html.H4(children="Please select the unit:",
                style={
                'textAlign': 'center'
                }),
        html.Div([
            dcc.Dropdown(
                id="unit_2",
                options=[{'label': i, 'value': i} for i in available_units],
                value="Chain linked volumes (2010), million euro"
            ),
        ],
            style={'width': '100%', 'display': 'inline-block', 'textAlign': 'center'}),
    ]),
    
    #graph 1
    html.Div([
        dcc.Graph(id="indicator-graphic2"),
    ]), 
])

#callback for output 1
@app.callback(
    dash.dependencies.Output("indicator-graphic1", "figure"),
    [dash.dependencies.Input("indicator_x1", "value"),
     dash.dependencies.Input("indicator_y1", "value"),
     dash.dependencies.Input('xaxis-type1', 'value'),
     dash.dependencies.Input('yaxis-type1', 'value'),
     dash.dependencies.Input('unit_1', 'value'),
     dash.dependencies.Input('year--slider1', 'value')])

def update_graph(indicator_x_name, indicator_y_name, 
                 xaxis_type, yaxis_type, unit,
                 year_value):
    dff=df[df["TIME"]==year_value]
    dff=df[df["UNIT"]==unit]
    
    return{
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == indicator_x_name]['Value'],
            y=dff[dff['NA_ITEM'] == indicator_y_name]['Value'],
            text=dff[dff['NA_ITEM'] == indicator_y_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': indicator_x_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': indicator_y_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

#callback for output 2
@app.callback(
    dash.dependencies.Output("indicator-graphic2", "figure"),
    [dash.dependencies.Input("countries", "value"),
     dash.dependencies.Input("indicator_y2", "value"),
     dash.dependencies.Input('yaxis-type2', 'value'),
     dash.dependencies.Input('unit_2', 'value')])

def update_graph(country, indicator_y_name, 
                 yaxis_type, unit):
    dff=df[df["GEO"]==country]
    dff=dff[dff["NA_ITEM"]==indicator_y_name]
    dff=dff[dff["UNIT"]==unit]
    
    return{
        'data': [go.Scatter(
            x=dff['TIME'],
            y=dff['Value'],
            mode='lines'
        )],
        'layout': go.Layout(
            xaxis={
                'title': "Year"
            },
            yaxis={
                'title': indicator_y_name+", "+unit,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()

