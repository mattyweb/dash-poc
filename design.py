
DISCRETE_COLORS = [
    '#267370', 
    '#8B508B', 
    '#EDAD08', 
    '#1D6996',
    '#11975F', 
    '#E17C05',
    '#685DB1',
    '#AE3D51', 
    '#79B74E', 
    '#BF82BA', 
    '#D05F4E',
]

LABELS = {
    "created_year": "Year",
    "created_month": "Month",
    "created_date": "Date Reported",
    "council_name": "Neighborhood",
    "type_name": "Request Type",
    "day_of_week": "Day of Week Reported",
    "counts": "Total Requests",
    "value": "Total Requests",
}

def apply_figure_style(fig):

    fig.update_layout(
        paper_bgcolor='#0F181F',
        plot_bgcolor='#29404F',
        title_x=0.5,
        title_yanchor='top',
        font_family="Roboto, Arial",
        font_color="#ECECEC",
        colorway=DISCRETE_COLORS,
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
