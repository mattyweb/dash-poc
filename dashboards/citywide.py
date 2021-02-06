import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app

import datetime

start_date = datetime.date.today() - datetime.timedelta(days=14)
end_date = datetime.date.today()

df = pd.read_json(f"https://dev-api.311-data.org/reports?start_date={start_date}&end_date={end_date}")

report_df = df.groupby(['created_date', 'type_name']).agg('sum').reset_index()

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
              title="TREND OF REQUESTS BY TYPE")

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
    tickmode = 'linear',
    ticks="outside",
    tickformat="%m/%d\n(%a)",
    title_font_color="#999999"
    )

fig.update_yaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='#1A2832',
    ticks="outside",
    tickformat=",",
    title_font_color="#999999"
    )

fig.update_traces(
    mode='markers+lines'
    )  # add markers to lines


pie_df = df.groupby(['type_name']).agg('sum').reset_index()

pie_fig = px.pie(pie_df,
              names="type_name", 
              values="counts",
              labels={
                "created_date": "Date Reported",
                "council_name": "Neighborhood",
                "type_name": "Request Type",
                "counts": "Total Requests"
              },
              title="REQUEST TYPES")

pie_fig.update_layout(
    paper_bgcolor='#0F181F',
    plot_bgcolor='#29404F',
    title_x=0.5,
    title_yanchor='top',
    font_family="Roboto, Arial",
    font_color="#ECECEC",
)

df['created_date'] = pd.to_datetime(df['created_date'])
pie2_df = df.groupby(['created_date']).agg('sum').reset_index()
pie2_df['day_of_week'] = pie2_df['created_date'].dt.day_name()

pie2_fig = px.pie(pie2_df,
              names="day_of_week", 
              values="counts",
              labels={
                "created_date": "Date Reported",
                "council_name": "Neighborhood",
                "type_name": "Request Type",
                "counts": "Total Requests"
              },
              title="DAY OF WEEK")

pie2_fig.update_layout(
    paper_bgcolor='#0F181F',
    plot_bgcolor='#29404F',
    title_x=0.5,
    title_yanchor='top',
    font_family="Roboto, Arial",
    font_color="#ECECEC",
)

layout = html.Div([
    html.Div([
        html.Span("Total requests: ", className="labelDiv"),
        html.Span(report_df['counts'].sum(), className="dataDiv"),
    ]),
    html.Div([
        html.Span("Date range: ", className="labelDiv"),
        html.Span(f"{start_date} to {end_date}", className="dataDiv"),
    ]),
    dcc.Graph(id='graph', figure=fig),
    dcc.Graph(id='graph2', figure=pie_fig, className="halfGraph"),
    dcc.Graph(id='graph3', figure=pie2_fig, className="halfGraph")
])
