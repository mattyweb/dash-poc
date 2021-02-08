import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from design import DISCRETE_COLORS, LABELS, apply_figure_style
from app import app


# TITLE
title = "NEIGHBORHOODS"

# DATA
df = pd.read_json('https://dev-api.311-data.org/reports?field=type_name&field=council_name&field=created_date')

fig = px.line()
apply_figure_style(fig)

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

# Define callback to update graph
@app.callback(
    Output('graph1', 'figure'),
    [Input("council_list", "value")]
)
def update_figure(selected_council):
    
    neighborhood_sum_df = df[df.council_name == selected_council].groupby(['created_date']).agg('sum').reset_index()
    total_sum_df = df.groupby(['created_date']).agg('sum').reset_index()
    total_sum_df["nc_avg"] = total_sum_df["counts"]/99
    merged_df = neighborhood_sum_df.merge(total_sum_df["nc_avg"].to_frame(), left_index=True, right_index=True)

    fig = px.line(merged_df,
                  x="created_date", 
                  y=['counts', 'nc_avg'],
                  color_discrete_sequence=DISCRETE_COLORS,
                  labels=LABELS,
                  title="Comparison trend for " + selected_council)

    fig.update_xaxes(
        tickformat="%a\n%m/%d",
    )

    fig.update_traces(
        mode='markers+lines'
    )  # add markers to lines

    apply_figure_style(fig)

    return fig


# Define callback to update graph
@app.callback(
    Output('graph2', 'figure'),
    [Input("council_list", "value")]
)
def update_figure(selected_council):
    
    report_df = df[df.council_name == selected_council].groupby(['created_date', 'type_name']).agg('sum').reset_index()

    fig = px.line(report_df,
                  x="created_date", 
                  y="counts",
                  color="type_name",
                  color_discrete_sequence=DISCRETE_COLORS,
                  labels=LABELS,
                  title="Request type trend for " + selected_council)

    fig.update_xaxes(
        tickformat="%a\n%m/%d",
        )

    fig.update_traces(
        mode='markers+lines'
        )  # add markers to lines

    apply_figure_style(fig)

    return fig


layout = html.Div([
    html.H1(title),
    dcc.Dropdown(
        id='council_list', 
        clearable=False,
        value="Arleta",
        placeholder="Select a neighborhood",
        options=populate_options()
    ),
    dcc.Graph(
        id='graph1',
        figure=fig
    ),
    dcc.Graph(
        id='graph2',
        figure=fig
    )
])
