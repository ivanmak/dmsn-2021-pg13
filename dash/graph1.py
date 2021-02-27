
import math
from datetime import datetime, timedelta

import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import plotly.express as px

import dash
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# Read CSV file
df = pd.read_csv('../soc-sign-bitcoinotc.csv', header=None)
df.columns = [ 'source', 'target', 'rating', 'time' ]

# Convert timestamp to date
df['time'] = pd.to_datetime(df['time'].astype(int), unit='s') 

df = df.sort_values(by='time').reset_index().drop(['index'], axis=1)
df['second'] = df['time'] - df['time'][0]
df['second'] = df['second'].apply(lambda x: math.floor(x.total_seconds()))
df['date'] = df['time'].apply(lambda x: x.replace(hour=0, minute=0, second=0, microsecond=0))

# Create graph
G = nx.MultiDiGraph()
for line in df[(df['time'] >= datetime(2010,11,8)) & (df['time'] < datetime(2010,11,30))].values:
    G.add_edge(line[0], line[1], weight=int(line[2]))
    
element_list = []
stylesheet_list = []
for n in G.nodes():
    element_list.append({
        'data': {
            'id': 'node_{}'.format(n),
            'label': 'Node {}'.format(n)
        }
    })

for i, e in enumerate(G.edges(data=True)):
    element_list.append({
        'data': {
            'id': 'edge_{}'.format(i),
            'source': 'node_{}'.format(e[0]),
            'target': 'node_{}'.format(e[1])
        }
    })
    
    style = {
        'selector': '#edge_{}'.format(i),
        'style': {
            'label': e[2]['weight'],
            'line-color': 'grey',
            'target-arrow-color': 'grey'
        }
    }
    if e[2]['weight'] >= -10 and e[2]['weight'] <= -6:
        style['style']['line-color'] = 'red'
        style['style']['target-arrow-color'] = 'red'
        
    elif e[2]['weight'] >= -5 and e[2]['weight'] <= -1:
        style['style']['line-color'] = 'orange'
        style['style']['target-arrow-color'] = 'orange'
        
    elif e[2]['weight'] == 0:
        style['style']['line-color'] = 'grey'
        style['style']['target-arrow-color'] = 'grey'
        
    elif e[2]['weight'] >= 1 and e[2]['weight'] <= 5:
        style['style']['line-color'] = 'brown'
        style['style']['target-arrow-color'] = 'brown'
        
    elif e[2]['weight'] >= 6:
        style['style']['line-color'] = 'green'
        style['style']['target-arrow-color'] = 'green'
        
    #print(style)
    stylesheet_list.append(style)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        layout={'name': 'cose'},
        style={'width': '100%', 'height': '960px'},
        elements=element_list,
        stylesheet=[
            {
                'selector': 'edge',
                'style': {
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier'
                }
            },
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)'
                }
            }
        ] + stylesheet_list
    )
])

app.run_server(debug=True)
