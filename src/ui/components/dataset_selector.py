from dash import dcc
import dash_bootstrap_components as dbc
import models.helpers.slug as sl
import globals


def render(
        dropdown_id: str,
        dataset_kind: str = 'timesheet',
        default_option: str = 'timesheet-last-six-weeks'
):
    dropdown_options = [
        {
            'label': f"{dataset['kind']} - {dataset['name']}",
            'value': sl.generate(f"{dataset['kind']} - {dataset['name']}")
        }
        for dataset in globals.datasets.get_datasets()
        if dataset['kind'].lower() == dataset_kind.lower()
    ]

    return dbc.Card(
        children=[
            dbc.CardHeader('Dataset'),
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id=dropdown_id,
                        options=dropdown_options,
                        placeholder="Select a dataset",
                        value=default_option
                    ),
                ], style={'padding': '10px'}
            )]
    )