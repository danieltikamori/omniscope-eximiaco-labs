import dash
from dash import html
import dash_bootstrap_components as dbc
import ui.components.base.title as title
import ui.components.cases_summary as cs
from datetime import datetime

import ui.components.case_card as cc
import globals

dash.register_page(__name__, title='Omniscope')


def layout(**kwargs):
    active_cases = globals.omni.cases.get_active_cases()
    summary = cs.render(active_cases)

    active_cases_cards = [
        cc.render(case)
        for case in active_cases
    ]

    return html.Div(
        [
            summary,
            title.render('Our Active Cases'),
            dbc.Row(active_cases_cards, justify='center')
        ],
        style={'padding': '20px'}
    )