import os, signal
import re
import glob
import importlib
import logging

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from config import PRELOAD, DASH_FILES


server = app.server
logger = logging.getLogger("gunicorn.error")
available_dashboards = []


files = glob.glob(f"{DASH_FILES}/*.py")
files.remove('dashboards/__init__.py')

for file in files:
    file = re.search("([\w]*)(.py)", file)
    dash_mod = file.group(1)
    available_dashboards.append(dash_mod)


if PRELOAD:
    logger.log(logging.INFO, f"Installing dashboards: { ', '.join(available_dashboards) }")

    for i in available_dashboards:
        module = importlib.import_module(f"{DASH_FILES}.{i}")


# callback to handle requests
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):

    last_part = re.search("([\w]*)$", pathname).group(1)

    # run the dashboard
    if last_part in available_dashboards:
        logger.log(logging.INFO, f"Running dashboard: {last_part}")
        module = importlib.import_module(f"{DASH_FILES}.{last_part}")
        return module.layout
    
    # terminate/reload the worker (and reload dashboards)
    elif last_part == 'reload':
        logger.log(logging.WARNING, "Report Server reload requested")
        os.kill(os.getpid(), signal.SIGTERM)
        return html.Div('Reloading...')
    
    # show links to each dashboard
    else:
        logger.log(logging.INFO, "Loading dashboard list")
        return html.Div([
            dcc.Link(dashboard, href=f"/{DASH_FILES}/{dashboard}") for dashboard in available_dashboards
        ], className="dash-links")


logger.log(logging.INFO, f"Report Server ready")


if __name__ == '__main__':
    app.run_server(debug=True)
