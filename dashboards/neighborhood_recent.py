import pandas as pd

import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from config import API_HOST


pretty_columns = {
    'srnumber': "SR Number", 
    'createdDate': "Created Date", 
    'closedDate': "Closed Date", 
    'typeName': "Type Name", 
    'address': "Address"
}

# TITLE
title = "NEIGHBORHOOD RECENT DATA"

# DATA
query_string = '/requests/updated'
df = pd.read_json(API_HOST + query_string)

table_df = df.query(f"councilName == 'Arleta'")[['srnumber', 'createdDate', 'closedDate', 'typeName', 'address']]


# Populate the neighborhood dropdown
def populate_options():
    council_df = pd.read_json('https://dev-api.311-data.org/councils')
    values = []
    for i in council_df.sort_values('councilName').councilName.unique():
        values.append(
            {
              'label': i,
              'value': i
            }
        )
    return values


# Define callback to update graph
@app.callback(
    Output("council_table", "data"),
    [Input("council_list", "value")]
)
def update_figure(selected_council):    
    table_df = df.query(f"councilName == '{selected_council}'")[['srnumber', 'createdDate', 'closedDate', 'typeName', 'address']]
    return table_df.to_dict('records')


# Layout
layout = html.Div([
    html.H1(title),
    dcc.Dropdown(
        id='council_list', 
        clearable=False,
        value="Arleta",
        placeholder="Select a neighborhood",
        options=populate_options()
    ),
    dash_table.DataTable(        
        id='council_table',
        columns=[{"name": pretty_columns[i], "id": i} for i in table_df.columns],
        style_as_list_view=True,
        style_cell={
            'padding': '5px',
            'textAlign': 'left',
            'fontFamily': 'Roboto, Arial',
            'fontSize': 12,
            'color': '#333333',
        },
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        sort_action='native',
        # filter_action='native',
        page_size=20,
    )
])
