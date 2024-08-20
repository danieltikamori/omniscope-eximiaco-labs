import dash
from dash import html, dcc, callback, Input, Output, State

import globals
import ui.components.allocation_by_case as by_case
import ui.components.allocation_by_client as abc
import ui.components.allocation_by_kind as abk
import ui.components.allocation_by_worker as abw
import ui.components.allocation_by_working_day as abwd
import ui.components.dataset_selector as selector
import ui.components.last_six_weeks_work_summary as lswws
import ui.components.headers.worker_header as wh

dash.register_page(__name__, path_template="/account-managers/<slug>", title='Omniscope')


def layout(slug: str):
    am = globals.omni.workers.get_by_slug(slug)

    result = html.Div(
        [
            dcc.Store('am-slug-store', data=slug),
            wh.render(am),
            selector.render('am-datasets-dropdown'),
            html.Div(id='am-content-area'),
        ]
    )

    return result


@callback(
    Output('am-content-area', 'children'),
    Input('am-datasets-dropdown', 'value'),
    [State('am-slug-store', 'data')]
)
def update_content_area(dataset_slug: str, slug: str, **kwargs):

    ap = (globals.datasets.get_by_slug(dataset_slug)
          .filter_by(by='AccountManagerSlug', equals_to=slug)
          )

    children = [
        abk.render(ap.data),
        html.Hr(style={'marginBottom': '10px', 'marginTop': '10px'}),
        abc.render(ap.data),
        html.Hr(style={'marginBottom': '10px', 'marginTop': '10px'}),
        abwd.render(ap.data),
        lswws.render(ap, dataset_slug),
        html.Hr(style={'marginBottom': '10px', 'marginTop': '10px'}),
        abw.render(ap.data),
        html.Hr(style={'marginBottom': '10px', 'marginTop': '10px'}),
        by_case.render(ap.data)
    ]

    return html.Div(children)
