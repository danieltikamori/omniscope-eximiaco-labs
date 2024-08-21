from dash import html
import pandas as pd
import dash_bootstrap_components as dbc

import ui.components.base.cards as c
import ui.components.allocation.timesheet_field_graph as tfg

from models.datasets.timesheet_dataset import TimeSheetFieldSummary


def render(data: pd.DataFrame):
    if len(data) == 0:
        return html.Div()

    tfs = TimeSheetFieldSummary(data, 'ClientName')

    return html.Div(
        [
            dbc.Row(
                [
                    c.create_kpi_card('Unique Clients', tfs.unique, 4),
                    c.create_kpi_card('Avg. Hours per Client', f'{tfs.avg_hours:.1f} hrs', 4),
                    c.create_kpi_card('Std. Hours per Client', f'{tfs.std_hours:.1f}', 4),
                ], style={'marginBottom': '10px'}
            ),
            dbc.Row(tfg.render(tfs, 'Hours Allocated by Client and Work Type', 'Client'))
        ]
    )
