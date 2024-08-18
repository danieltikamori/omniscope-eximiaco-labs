import dash
import dash_bootstrap_components as dbc
from dash import html

import globals
import ui.components.base.datagrid as datagrid
import ui.components.base.title as title

import ui.components.weekly_projected_vs_actual_graph as wpa

dash.register_page(__name__, title='Omniscope')


def layout(**kwargs):
    publications = globals.datasets.ontology_entries.get_last_six_weeks()

    children = []

    if len(publications.data) == 0:
        return html.Div([])

    publications_by_author = publications.get_weekly_summary('Worker',
                                                             operation='count',
                                                             date_column='CreationDate',
                                                             week_column='CreationWeek')

    children.append(
        dbc.Row(
            dbc.Col(
                [
                    title.render(f'Ontology Publications by Author', 3),
                    wpa.render(publications_by_author),
                    datagrid.summary(f'slug_squads', publications_by_author)
                ]
            )
        )
    )

    publications_by_class = publications.get_weekly_summary('ClassName',
                                                            operation='count',
                                                            date_column='CreationDate',
                                                            week_column='CreationWeek')

    children.append(
        dbc.Row(
            dbc.Col(
                [
                    title.render(f'Ontology Publications by Class', 3),
                    datagrid.summary(f'slug_squads', publications_by_class)
                ]
            )
        )
    )

    return html.Div(children=children)