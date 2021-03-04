import datetime

import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html

from design import DISCRETE_COLORS, LABELS, apply_figure_style
from config import API_HOST


# TITLE
title = "RECENT 311 REQUESTS"

# DATA
start_date = datetime.date.today() - datetime.timedelta(days=15)
end_date = datetime.date.today() - datetime.timedelta(days=1)

query_string = f"/reports?filter=created_date>={start_date}&filter=created_date<={end_date}"
print(" * Downloading data for dataframe")
df = pd.read_json(API_HOST + query_string)
print(" * Dataframe has been loaded")

#FIGURES
report_df = df.groupby(['created_date', 'type_name']).agg('sum').reset_index()
fig = px.line(report_df,
              x="created_date", 
              y="counts",
              color="type_name",
              color_discrete_sequence=DISCRETE_COLORS,
              labels=LABELS,
              )

fig.update_xaxes(
    tickformat="%a\n%m/%d",
)

fig.update_traces(
    mode='markers+lines'
)  # add markers to lines


pie_df = df.groupby(['type_name']).agg('sum').reset_index()
pie_fig = px.pie(pie_df,
              names="type_name", 
              values="counts",
              color_discrete_sequence=DISCRETE_COLORS,
              labels=LABELS,
            )


df['created_date'] = pd.to_datetime(df['created_date'])
dow_df = df.groupby(['created_date']).agg('sum').reset_index()
dow_df['day_of_week'] = dow_df['created_date'].dt.day_name()
dow_fig = px.bar(dow_df,
              x="day_of_week", 
              y="counts",
              color_discrete_sequence=DISCRETE_COLORS,
              labels=LABELS,
            )

apply_figure_style(fig)
apply_figure_style(pie_fig)
apply_figure_style(dow_fig)

# LAYOUT
layout = html.Div([
    html.H1(title),
    html.Div([
        html.Div([html.H2(f"{report_df['counts'].sum():,}"), html.Label("Total Requests")], className="dataLabel"),
        html.Div([html.H2(f"{start_date.strftime('%b %d')}"), html.Label("Report Start Date")], className="dataLabel"),
        html.Div([html.H2(f"{end_date.strftime('%b %d')}"), html.Label("Report End Date")], className="dataLabel"),
    ], className="row"),
    dcc.Graph(id='graph', figure=fig),
    dcc.Graph(id='graph3', figure=dow_fig, className="halfGraph"),
    dcc.Graph(id='graph2', figure=pie_fig, className="halfGraph"),
])
