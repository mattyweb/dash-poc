import os, signal
import re
import glob
import importlib
import logging

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app


server = app.server
logger = logging.getLogger("gunicorn.error")
available_dashboards = []


# find and import files from /dashboards as modules
files = glob.glob("dashboards/*.py")
files.remove('dashboards/__init__.py')

for file in files:
    file = re.search("([\w]*)(.py)", file)
    dash_mod = file.group(1)
    available_dashboards.append(dash_mod)

logger.log(logging.INFO, f"Installing dashboards: { ', '.join(available_dashboards) }")

for i in available_dashboards:
    module = importlib.import_module(f"dashboards.{i}")

logger.log(logging.INFO, f"Report Server ready")


# set up default layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# callback to handle requests
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):

    last_part = re.search("([\w]*)$", pathname).group(1)

    # run the dashboard
    if last_part in available_dashboards:
        logger.log(logging.INFO, f"Running dashboard: {last_part}")
        module = importlib.import_module(f"dashboards.{last_part}")
        return module.layout
    
    # terminate/reload the worker (and reload dashboards)
    elif last_part == 'reload':
        logger.log(logging.WARNING, "Report Server reload requested")
        os.kill(os.getpid(), signal.SIGTERM)
    
    # show links to each dashboard
    else:
        return html.Div([
            dcc.Link(dashboard, href=f"/dashboards/{dashboard}") for dashboard in available_dashboards
        ], className="dashLinks")


if __name__ == '__main__':
    app.run_server(debug=True)
