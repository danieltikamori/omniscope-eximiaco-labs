import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import ui.components.client_card as cc

import globals
import ui.components.base.title as title

dash.register_page(__name__, title='Omniscope')


def layout(**kwargs):
    clients = sorted(globals.omni.clients.get_all().values(), key=lambda client: client.name)
    strategic_clients = [
        c for c in clients
        if c.is_strategic
    ]

    non_strategic_clients = [
        c for c in clients
        if not c.is_strategic
    ]

    return html.Div(
        [
            title.render('Our Strategic Clients', 3),
            dbc.Row(
                [
                    cc.render(client)
                    for client in strategic_clients
                ], justify='center'
            ),
            title.render('Other Clients', 3),
            dbc.Row(
                [
                    cc.render(client)
                    for client in non_strategic_clients
                ], justify='center'
            ),
        ],
        style={'padding': '20px'}  # Adicionando padding para dar espaço ao conteúdo
    )
