import dash_bootstrap_components as dbc
from dash import html, Dash


def run(dash_content):
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = dbc.Row(dash_content)
    app.run_server(mode='inline')
