from dash import html
import pandas as pd
import dash_bootstrap_components as dbc
import ui.components.base.cards as c

from models.datasets.timesheet_dataset import TimeSheetFieldSummary
import ui.components.allocation.timesheet_field_graph as tfg


def render(data: pd.DataFrame):
    if len(data) == 0:
        return html.Div()

    tfs = TimeSheetFieldSummary(data, 'WorkerName')

    return html.Div(
        [
            dbc.Row([
                c.create_kpi_card('Unique Workers', tfs.unique, 4),
                c.create_kpi_card('Avg. Hours per Worker', f'{tfs.avg_hours:.1f} hrs', 4),
                c.create_kpi_card('Std. Hours per Worker', f'{tfs.std_hours:.1f}', 4),
            ], style={'marginBottom': '10px'}),
            dbc.Row(tfg.render(tfs, 'All Workers by Hours', 'Workers')),
        ]
    )
