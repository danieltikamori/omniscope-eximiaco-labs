import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

import globals
import ui.components.product_or_service_card as pos_card
from models.domain import ProductOrService

import ui.components.base.title as title

dash.register_page(__name__, title='Omniscope')



def layout():
    items = globals.omni.products_or_services.get_all().values()

    return html.Div([
        title.render('Our Products or Services', level=3),
        dbc.Row(
            [
                pos_card.render(item)
                for item in items
            ]
        )
    ])
