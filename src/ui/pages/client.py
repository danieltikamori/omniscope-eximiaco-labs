import dash
from dash import html, dcc, Input, Output, State, callback

import globals
import ui.components.client_header as ch
import ui.components.weekly_projected_vs_actual_graph as wpa
import ui.components.allocation_by_kind_diary as abkd
import ui.components.dataset_selector as selector
import ui.components.allocation_by_kind as abk
import ui.components.allocation_by_working_day as abwd
import ui.components.allocation_by_worker as abw
import ui.components.allocation_by_case as by_case
import ui.components.last_six_weeks_work_summary as lswws

import ui.components.base.colors as colors
import ui.components.base.cards as c

dash.register_page(__name__, path_template="/clients/<slug>", title='Omniscope')


def layout(slug: str, **kwargs):
    client = globals.omni.clients.get_by_slug(slug)

    return html.Div(
        [
            dcc.Store('client-slug-store', data=slug),
            ch.render(client),
            selector.render('client-datasets-dropdown'),
            html.Div(id='client-content-area'),
        ]
    )


@callback(
    Output('client-content-area', 'children'),
    Input('client-datasets-dropdown', 'value'),
    [State('client-slug-store', 'data')]
)
def update_content_area(dataset_slug: str, slug: str, **kwargs):
    client = globals.omni.clients.get_by_slug(slug)

    ap = (globals.datasets.get_by_slug(dataset_slug)
          .filter_by(by='ClientId', equals_to=client.id)
          )

    return html.Div([
        abk.render(ap.data),
        html.Hr(style={'marginBottom': '10px', 'marginTop': '10px'}),
        abwd.render(ap.data),
        lswws.render(ap, dataset_slug),
        html.Hr(style={'marginBottom': '10px', 'marginTop': '10px'}),
        abw.render(ap.data),
        html.Hr(style={'marginBottom': '10px', 'marginTop': '10px'}),
        by_case.render(ap.data, include_sponsor=True)
    ])