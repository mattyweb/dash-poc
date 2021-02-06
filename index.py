import re
import glob
import importlib

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pkg_resources import to_filename

from app import app


server = app.server
available_dashboards = []

# find and import files from /dashboards as modules
files = glob.glob("dashboards/*.py")
files.remove('dashboards/__init__.py')

for file in files:
    file = re.search("([\w]*)(.py)", file)
    dash_mod = file.group(1)
    available_dashboards.append(dash_mod)

print(f"Installed dashboards: { ','.join(available_dashboards) }")


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    last_part = re.search("([\w]*)$", pathname)
    dash_mod = last_part.group(1)
    if dash_mod in available_dashboards:
        print(f"running {dash_mod} dashboard")
        module = importlib.import_module(f"dashboards.{dash_mod}")
        return module.layout
    elif dash_mod == 'dashboards':
        return f"[{ ','.join(available_dashboards) }]"
    else:
        return html.Div([
            dcc.Link(dashboard, href=f"/dashboards/{dashboard}") for dashboard in available_dashboards
        ], className="dashLinks")


if __name__ == '__main__':
    app.run_server(debug=True)
