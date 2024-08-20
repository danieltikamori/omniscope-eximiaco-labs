import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input, State, callback

import globals
import ui.components.allocation_by_case as by_case
import ui.components.allocation_by_client as abc
import ui.components.allocation_by_kind as abk
import ui.components.allocation_by_working_day as abwd
import ui.components.dataset_selector as selector
import ui.components.last_six_weeks_work_summary as lswws
import ui.components.headers.worker_header as wh


def _create_graph_card(title, graph):
    return dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody([graph])
        ], className="mb-4"
    )


dash.register_page(__name__, path_template="/consultants/<slug>", title='Omniscope')


def layout(slug: str, **kwargs):
    consultant = globals.omni.workers.get_by_slug(slug)

    result = html.Div(
        [
            dcc.Store('consultant-slug-store', data=slug),
            wh.render(consultant),
            selector.render('consultant-datasets-dropdown'),
            html.Div(id='consultant-content-area'),
        ]
    )

    return result


@callback(
    Output('consultant-content-area', 'children'),
    Input('consultant-datasets-dropdown', 'value'),
    [State('consultant-slug-store', 'data')]
)
def update_content_area(dataset_slug: str, slug: str, **kwargs):

    ap = (globals.datasets.get_by_slug(dataset_slug)
          .filter_by(by='WorkerSlug', equals_to=slug)
          )

    return html.Div([
        abk.render(ap.data),
        html.Hr(style={'marginBottom': '10px', 'marginTop': '10px'}),
        abc.render(ap.data),
        html.Hr(style={'marginBottom': '10px', 'marginTop': '10px'}),
        abwd.render(ap.data),
        lswws.render(ap, dataset_slug),
        html.Hr(style={'marginBottom': '10px', 'marginTop': '10px'}),
        by_case.render(ap.data)
    ])
