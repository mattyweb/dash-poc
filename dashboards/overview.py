import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from design import DISCRETE_COLORS, LABELS, apply_figure_style


# TITLE
title = "311 DATA OVERVIEW"

# DATA
df = pd.read_json('https://dev-api.311-data.org/reports?field=type_name&field=council_name&field=created_year&filter=created_date>=2016-01-01')
df['council_name'] = df['council_name'].str.slice(0,30)  # trim long councils

# FIGURES
# council figure
df1 = df.groupby(['council_name'])['counts'].sum().sort_values().to_frame()
fig1 = px.bar(
    df1,
    x=df1.index,
    y='counts',
    color_discrete_sequence=DISCRETE_COLORS,
    labels=LABELS,
)

# year totals figure
df2 = df.groupby(['created_year'])['counts'].sum().to_frame()
fig2 = px.bar(
    df2,
    x=df2.index,
    y='counts',
    color_discrete_sequence=DISCRETE_COLORS,
    labels=LABELS,
)

# types figure
df3 = df.groupby(['type_name'])['counts'].sum().to_frame()
fig3 = px.pie(
    df3,
    names=df3.index,
    values='counts',
    color_discrete_sequence=DISCRETE_COLORS,
    labels=LABELS,
)


stas_df = pd.read_json('https://dev-api.311-data.org/types/stats')
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
    dtick=5,
)

# apply shared styles
apply_figure_style(fig1)
apply_figure_style(fig2)
apply_figure_style(fig3)
apply_figure_style(fig4)

# LAYOUT
layout = html.Div([
    html.H1(title),
    html.Div([
        html.Div([html.H2(f"{df['counts'].sum():,}"), html.Label("Total Requests")], className="dataLabel"),
        html.Div([html.H2(f"{len(pd.unique(df['council_name']))}"), html.Label("Neighborhoods")], className="dataLabel"),
        html.Div([html.H2(f"{len(pd.unique(df['type_name']))}"), html.Label("Request Types")], className="dataLabel"),
    ], className="row"),
    html.Div([
        html.Div(dcc.Graph(id='graph2', figure=fig2), style={'display': 'inline-block', 'width': '50%'}),
        html.Div(dcc.Graph(id='graph3', figure=fig3), style={'display': 'inline-block', 'width': '50%'}),
    ]),
    dcc.Graph(id='graph4', figure=fig4),
    dcc.Graph(id='graph1', figure=fig1),
])
