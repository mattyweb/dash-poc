
DISCRETE_COLORS = [
    '#267370', 
    '#8B508B', 
    '#EDAD08', 
    '#1D6996',
    '#D05F4E', 
    '#BF82BA', 
    '#11975F', 
    '#AE3D51', 
    '#E17C05',
    '#79B74E', 
    '#685DB1',
]

LABELS = {
    "created_date": "Date Reported",
    "created_year": "Year",
    "created_month": "Month",
    "council_name": "Neighborhood",
    "type_name": "Request Type",
    "counts": "Total Requests",
    "value": "Total Requests",
    "day_of_week": "Reported Day of Week",
}

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
        