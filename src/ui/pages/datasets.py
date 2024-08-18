import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
from dash import callback, dcc, html, Input, Output, ALL
import plotly.express as px

import globals
import models.helpers.slug as slug

dash.register_page(__name__, path_template="/datasets", title='Omniscope')
dash.register_page(__name__, path_template="/datasets", title='Omniscope')


def __render_dataframe_to(dataset_slug: str, df: pd.DataFrame, columns_to_display=None, style=None):
    if not style:
        style = {}

    style['width'] = '100%'
    style['margin-top'] = '5px'

    def generate_column_defs(df, columns_to_display):
        columns = columns_to_display if columns_to_display else df.columns
        return [{'field': col, 'headerName': col, 'unsafe_allow_html': True} for col in columns]

    def generate_records(df, columns_to_display):
        return df[columns_to_display].to_dict(orient='records') if columns_to_display else df.to_dict(orient='records')

    grid = dag.AgGrid(
        id='dataset-records',
        rowData=generate_records(df, columns_to_display),
        columnDefs=generate_column_defs(df, columns_to_display),
        defaultColDef={"filter": True},
        dashGridOptions={
            'animateRows': False,
            'rowSelection': 'single',
            'getRowId': {'params': {'key': df.columns[0]}}
        },
        csvExportParams={
            "fileName": f"{dataset_slug}.csv",
        },
        style=style,
    )

    return html.Div(
        [
            html.Button("Download CSV", id="csv-button", n_clicks=0),
            grid]
    )


def layout(name: str = None, **kwargs):
    dropdown_options = [
        {
            'label': f"{dataset['kind']} - {dataset['name']}",
            'value': slug.generate(f"{dataset['kind']} - {dataset['name']}")
        } for dataset in globals.datasets.get_datasets()
    ]

    dataset_dropdown = dbc.Card(
        children=[
            dbc.CardHeader('Dataset'),
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id='datasets-dropdown',
                        options=dropdown_options,
                        placeholder="Select a dataset",
                        value=name
                    ),
                ], style={'padding': '10px'}
            )]
    )

    result = html.Div(
        [
            dataset_dropdown,
            dcc.Store(id='dataset-slug-store'),
            html.Div(id='filters-area'),
            dbc.Card(
                children=[
                    dbc.CardHeader('Output'),

                    dbc.CardBody(
                        [
                            dbc.Accordion(
                                children=[
                                    dbc.AccordionItem(
                                        [
                                            html.Div(id='path-fields-area'),
                                            html.Div(id='treemap-area', style={'margin-top': '5px'})
                                        ], title='TreeMap'
                                    ),
                                    dbc.AccordionItem(
                                        [
                                            html.Div(id='fields-area'),
                                            html.Div(id='records-area')
                                        ], title='Records'
                                    ),
                                ], always_open=True
                            )
                        ], style={'padding': '10px'}
                    )], style={'margin-top': '10px'}
            ),
        ]
    )

    return result


def get_dataframe(dataset_slug: str):
    return globals.datasets.get_by_slug(dataset_slug)


@callback(
    Output('dataset-slug-store', 'data'),
    Output('path-fields-area', 'children'),
    Output('fields-area', 'children'),
    Input('datasets-dropdown', 'value'),
)
def update_fields_area(dataset_slug: str):
    dss = globals.datasets.get_dataset_source_by_slug(dataset_slug)
    if not dss:
        return None, None

    options = [{'label': col, 'value': col} for col in dss.get_all_fields()]
    _, value = dss.get_treemap_path()
    path_fields_dropdown = dcc.Dropdown(
        id='path-fields-dropdown',
        options=options,
        value=value,
        placeholder="Areas",
        multi=True
    )

    options = [{'label': col, 'value': col} for col in dss.get_all_fields()]
    value = dss.get_common_fields()
    fields_dropdown = dcc.Dropdown(
        id='fields-dropdown',
        options=options,
        value=value,
        placeholder="Fields to display",
        multi=True
    )

    return dataset_slug, path_fields_dropdown, fields_dropdown


@callback(
    Output('filters-area', 'children'),
    Output('treemap-area', 'children'),
    Output('records-area', 'children'),
    Input('path-fields-dropdown', 'value'),
    Input('fields-dropdown', 'value'),
    Input('dataset-slug-store', 'data'),
    Input({'type': 'filter-dropdown', 'index': ALL}, 'value')
)
def update_datasets_output(path, columns, dataset_slug, filter_values):
    source = globals.datasets.get_dataset_source_by_slug(dataset_slug)
    df = get_dataframe(dataset_slug)
    data: pd.DataFrame = df.data

    filterable_fields = source.get_filterable_fields()
    active_filters = dict(zip(filterable_fields, filter_values))

    filters = []

    for filter in filterable_fields:
        filter_value = active_filters.get(filter, None)

        if len(data) > 0:
            row = dbc.Row(
                [
                    dbc.Col(html.P(filter), xs=12, sm=4, md=2, lg=2, xl=2, className='align-self-center'),
                    dbc.Col(
                        dcc.Dropdown(
                            id={'type': 'filter-dropdown', 'index': filter},
                            options=[{'label': val, 'value': val} for val in data[filter].drop_duplicates().sort_values()],
                            multi=True,
                            value=active_filters.get(filter, None),
                            placeholder=f"Filter by {filter}"
                        ), xs=12, sm=8, md=10, lg=10, xl=10, className='align-self-center'
                    )
                ], className='align-items-center', style={'margin-bottom': '10px'}
            )

            filters.append(row)
            if filter_value:
                data = data[data[filter].isin(filter_value)]

    filters_area = dbc.Card(
        children=[
            dbc.CardHeader('Filters'),
            dbc.CardBody(
                filters, style={'padding': '10px'}
            )], style={'margin-top': '10px'}
    )

    data['All'] = 'All'
    data['Unit'] = 1
    ag_value, _ = source.get_treemap_path()

    try:
        fig = px.treemap(data, path=['All'] + path, values=ag_value)
        fig.update_traces(textinfo="label+value+percent parent+percent root")
        fig.update_traces(root_color="lightgrey", marker=dict(cornerradius=3))
        fig.update_layout(margin=dict(t=25, l=10, r=10, b=10))
        treemap_area = dcc.Graph(figure=fig)
    except Exception as e:
        treemap_area = html.Div(f'Unable to create a treemap view ({e})', style={'margin-top': '10px'})

    records_area = html.Div(
        [
            __render_dataframe_to(dataset_slug, data, columns),
        ]
    )

    return filters_area, treemap_area, records_area


@callback(
    Output("dataset-records", "exportDataAsCsv"),
    Input("csv-button", "n_clicks"),
)
def export_data_as_csv(n_clicks):
    if n_clicks:
        return True
    return False
