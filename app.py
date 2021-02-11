import dash
import dash_html_components as html


external_stylesheets = ['/static/reports.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
app.config.suppress_callback_exceptions = True
