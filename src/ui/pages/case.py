import dash
from dash import html, dcc, Input, Output, State, callback

import globals
import ui.components.allocation_by_kind as abk
import ui.components.allocation_by_worker as abw
import ui.components.allocation_by_working_day as abwd
import ui.components.case_header as ch
import ui.components.dataset_selector as selector
import ui.components.last_six_weeks_work_summary as lswws

dash.register_page(__name__, path_template="/cases/<slug>", title='Omniscope')


def layout(slug: str, **kwargs):
    c = globals.omni.cases.get_by_slug(slug)
    return html.Div(
        [
            dcc.Store('case-slug-store', data=slug),
            ch.render(c),
            selector.render('case-datasets-dropdown'),
            html.Div(id='case-content-area'),
        ]
    )


@callback(
    Output('case-content-area', 'children'),
    Input('case-datasets-dropdown', 'value'),
    [State('case-slug-store', 'data')]
)
def update_content_area(dataset_slug: str, slug: str, **kwargs):
    c = globals.omni.cases.get_by_slug(slug)

    ap = (globals.datasets.get_by_slug(dataset_slug)
          .filter_by(by='CaseId', equals_to=c.id)
          )

    return html.Div(
        [
            abk.render(ap.data),
            html.Hr(style={'marginBottom': '10px', 'marginTop': '10px'}),
            abwd.render(ap.data),
            lswws.render(ap, dataset_slug),
            html.Hr(style={'marginBottom': '10px', 'marginTop': '10px'}),
            abw.render(ap.data)
        ]
    )