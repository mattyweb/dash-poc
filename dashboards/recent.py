import datetime
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html


# TITLE
title = "RECENT 311 REQUESTS"

# STYLING
discrete_colors = [
            '#267370', '#11975F', '#BF82BA', '#EDAD08', 
            '#79B74E', '#D05F4E', '#AE3D51', '#685DB1',
            '#8B508B', '#1D6996', '#E17C05'
            ]

def apply_figure_style(fig):
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
        title_font_color="#999999"
        )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#1A2832',
        ticks="outside",
        title_font_color="#999999"
        )

# DATA
start_date = datetime.date.today() - datetime.timedelta(days=14)
end_date = datetime.date.today() - datetime.timedelta(days=1)

df = pd.read_json(f"https://dev-api.311-data.org/reports?filter=created_date>={start_date}&filter=created_date<={end_date}")


#FIGURES
report_df = df.groupby(['created_date', 'type_name']).agg('sum').reset_index()

fig = px.line(report_df,
              x="created_date", 
              y="counts",
              color="type_name",
              color_discrete_sequence=discrete_colors,
              labels={
                "created_date": "Date Reported",
                "council_name": "Neighborhood",
                "type_name": "Request Type",
                "counts": "Total Requests"
              },
              )

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
              color_discrete_sequence=discrete_colors,
              labels={
                "created_date": "Date Reported",
                "council_name": "Neighborhood",
                "type_name": "Request Type",
                "counts": "Total Requests"
              },
            )


df['created_date'] = pd.to_datetime(df['created_date'])
dow_df = df.groupby(['created_date']).agg('sum').reset_index()
dow_df['day_of_week'] = dow_df['created_date'].dt.day_name()
dow_fig = px.bar(dow_df,
              x="day_of_week", 
              y="counts",
              color_discrete_sequence=discrete_colors,
              labels={
                "created_date": "Date Reported",
                "council_name": "Neighborhood",
                "day_of_week": "Request Day of Week",
                "counts": "Total Requests"
              },
            )


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
