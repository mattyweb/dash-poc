import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app


df = pd.read_json('https://dev-api.311-data.org/reports?start_date=2021-01-21&end_date=2021-02-04')

fig = px.line()

def populate_options():
    values = []
    for i in df.sort_values('council_name').council_name.unique():
        values.append(
            {
              'label': i,
              'value': i
            }
        )
    return values

layout = html.Div([
    dcc.Dropdown(
        id='council_list', 
        clearable=False,
        value="Arleta",
        placeholder="Select a neighborhood",
        options=populate_options()
    ),
    dcc.Graph(
        id='graph',
        figure=fig
    )
])

# Define callback to update graph
@app.callback(
    Output('graph', 'figure'),
    [Input("council_list", "value")]
)
def update_figure(selected_council):
    
    report_df = df[df.council_name == selected_council].groupby(['created_date', 'type_name']).agg('sum').reset_index()
    
    fig = px.line(report_df,
                  x="created_date", 
                  y="counts",
                  color="type_name",
                  labels={
                    "created_date": "Date Reported",
                    "council_name": "Neighborhood",
                    "type_name": "Request Type",
                    "counts": "Total Requests"
                  },
                  title="Request type trend for " + selected_council)
    
    fig.update_layout(
        paper_bgcolor='#0F181F',
        plot_bgcolor='#29404F',
        title_x=0.5,
        title_yanchor='top',
        font_family="Roboto, Arial",
        font_color="#ECECEC",
    )

    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#1A2832',
        ticks="outside",
        tickmode = 'linear',
        tickformat="%a\n%m/%d",
        )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#1A2832',
        ticks="outside",
        tickformat=","
        )

    fig.update_traces(
        mode='markers+lines'
        )  # add markers to lines

    return fig
