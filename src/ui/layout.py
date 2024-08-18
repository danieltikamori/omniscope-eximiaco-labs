import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from ui.components import navbar


def render():
    return html.Div(
        children=[
            dcc.Location(id='url', refresh=True),
            navbar.render(),
            dcc.Loading(
                dbc.Container(
                    dash.page_container,
                    style={'margin-top': '50px'},
                    className="dbc dbc-ag-grid"
                ),
                overlay_style={"visibility": "visible", "filter": "blur(2px)"},
            )
        ],
        style={'backgroundColor': dbc.themes.BOOTSTRAP},
    )
