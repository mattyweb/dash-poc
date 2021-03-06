import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

from config import API_HOST
from design import DISCRETE_COLORS, LABELS, apply_figure_style


# TITLE
title = "311 DATA OVERVIEW"

# FIGURES
# council figure
print(" * Downloading data for dataframe")
query_string = "/reports?field=council_name&filter=created_date>=2016-01-01"
df1 = pd.read_json(API_HOST + query_string)
df1 = df1.groupby(['council_name'])['counts'].sum().sort_values().to_frame()
fig1 = px.bar(
    df1,
    x=df1.index,
    y='counts',
    color_discrete_sequence=DISCRETE_COLORS,
    labels=LABELS,
)

# year totals figure
print(" * Downloading data for dataframe")
query_string = "/reports?field=created_year&filter=created_date>=2016-01-01"
df2 = pd.read_json(API_HOST + query_string)
df2 = df2.groupby(['created_year'])['counts'].sum().to_frame()
fig2 = px.bar(
    df2,
    x=df2.index,
    y='counts',
    color_discrete_sequence=['#1D6996'],
    labels=LABELS,
)

# agency figure
print(" * Downloading data for dataframe")
query_string = "/reports?field=agency_name&filter=created_date>=2016-01-01"
df5 = pd.read_json(API_HOST + query_string)
df5 = df5.groupby(['agency_name'])['counts'].sum().to_frame()
df5.sort_values('counts', ascending=False, inplace=True)
df5.loc['Others'] = df5[5:].sum()
df5.sort_values('counts', ascending=False, inplace=True)
df5 = df5[:6]
fig5 = px.pie(
    df5,
    names=df5.index,
    values='counts',
    color_discrete_sequence=DISCRETE_COLORS,
    labels=LABELS,
)

# source figure
print(" * Downloading data for dataframe")
query_string = "/reports?field=source_name&filter=created_date>=2016-01-01"
df6 = pd.read_json(API_HOST + query_string)
df6 = df6.groupby(['source_name'])['counts'].sum().to_frame()
df6.sort_values('counts', ascending=False, inplace=True)
df6.loc['Others'] = df6[5:].sum()
df6.sort_values('counts', ascending=False, inplace=True)
df6 = df6[:6]
fig6 = px.bar(
    df6,
    x=df6.index,
    y='counts',
    color_discrete_sequence=['#1D6996'],
    labels=LABELS,
)
# fig6 = px.pie(
#     df6,
#     names=df6.index,
#     values='counts',
#     color_discrete_sequence=DISCRETE_COLORS,
#     labels=LABELS,
# )

# types figure
print(" * Downloading data for dataframe")
query_string = "/reports?field=type_name&filter=created_date>=2016-01-01"
df3 = pd.read_json(API_HOST + query_string)
df3 = df3.groupby(['type_name'])['counts'].sum().to_frame()
fig3 = px.pie(
    df3,
    names=df3.index,
    values='counts',
    color_discrete_sequence=DISCRETE_COLORS,
    labels=LABELS,
)

stas_df = pd.read_json(API_HOST + '/types/stats')
stas_df = stas_df.sort_values('median', ascending=False)

fig4 = go.Figure()

fig4.add_trace(
    go.Box(
        y=stas_df.type_name,
        q1=stas_df['q1'], 
        median=stas_df['median'],
        q3=stas_df['q3'], 
        marker_color='#29404F',
        fillcolor='#E17C05'
    )
)

fig4.update_xaxes(
    title="Median Days to Close",
    dtick=5
)

# apply shared styles
apply_figure_style(fig1)
apply_figure_style(fig2)
apply_figure_style(fig3)
apply_figure_style(fig4)
apply_figure_style(fig5)
apply_figure_style(fig6)

# LAYOUT
layout = html.Div([
    html.H1(title),
    html.Div([
        html.Div([html.H2(f"{df2['counts'].sum():,}"), html.Label("Total Requests")], className="dataLabel"),
        html.Div([html.H2(df1.shape[0] - 1), html.Label("Neighborhoods")], className="dataLabel"),
        html.Div([html.H2(df3.shape[0]), html.Label("Request Types")], className="dataLabel"),
    ], className="row"),
    html.Div([
        html.Div(dcc.Graph(id='graph2', figure=fig2), style={'display': 'inline-block', 'width': '50%'}),
        html.Div(dcc.Graph(id='graph3', figure=fig3), style={'display': 'inline-block', 'width': '50%'}),
    ]),
    dcc.Graph(id='graph4', figure=fig4),
    html.Div([
        html.Div(dcc.Graph(id='graph5', figure=fig5), style={'display': 'inline-block', 'width': '50%'}),
        html.Div(dcc.Graph(id='graph6', figure=fig6), style={'display': 'inline-block', 'width': '50%'}),
    ]),
    dcc.Graph(id='graph1', figure=fig1),
])
