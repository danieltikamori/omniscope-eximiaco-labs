import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

import globals
from models.domain import ProductOrService

import ui.components.base.title as title

dash.register_page(__name__, title='Omniscope')


def create_product_or_service_card(ps: ProductOrService):
    return dbc.Col(
        dbc.Card(
            [
                dbc.CardImg(src=ps.cover_image_url, style={'width': 'auto'}, top=True),
                dbc.CardBody(
                    [
                        dcc.Markdown(ps.name, dangerously_allow_html=True)
                    ]
                )
            ], style={'margin': '10px'}
        ),
        xs=12, sm=6, md=4, lg=3, xl=3
    )


def layout():
    items = globals.omni.products_or_services.get_all().values()

    return html.Div([
        title.render('Our Products or Services', level=3),
        dbc.Row(
            [
                create_product_or_service_card(item)
                for item in items
            ]
        )
    ])
