import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html


# TITLE
title = "311 DATA OVERVIEW"

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
df = pd.read_json('https://dev-api.311-data.org/reports?field=type_name&field=council_name&field=created_year&filter=created_date>=2016-01-01')
df['council_name'] = df['council_name'].str.slice(0,30)  # trim long councils

# FIGURES
# council figure
df1 = df.groupby(['council_name'])['counts'].sum().sort_values().to_frame()
fig1 = px.bar(df1,
                x=df1.index,
                y='counts',
                color_discrete_sequence=discrete_colors,
                labels={
                  "counts": "Total Requests",
                  "council_name": "Neighborhoods"
                },
              )

# year totals figure
df2 = df.groupby(['created_year'])['counts'].sum().to_frame()
fig2 = px.bar(df2,
                x=df2.index,
                y='counts',
                color_discrete_sequence=discrete_colors,
                labels={
                  "counts": "Total Requests",
                  "created_year": "Years"
                },
              )

# types figure
df3 = df.groupby(['type_name'])['counts'].sum().to_frame()
fig3 = px.pie(df3,
                names=df3.index,
                values='counts',
                color_discrete_sequence=discrete_colors,
                labels={
                  "counts": "Total Requests",
                  "x": "Request Types"
                },
              )

# apply shared styles
apply_figure_style(fig1)
apply_figure_style(fig2)
apply_figure_style(fig3)

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
    dcc.Graph(id='graph1', figure=fig1),
])
