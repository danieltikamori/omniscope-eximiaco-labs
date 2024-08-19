import dash
import ast
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
import pandas as pd
from dash_bootstrap_components import Card

import globals

from models.helpers.weeks import Weeks
import models.datasets.timesheet_dataset as tsds

import ui.components.base.cards as c
import ui.components.base.title as title
import ui.components.allocation_sidebyside_table as asbst
from ui.helpers.beaulty import format_date_with_suffix


dash.register_page(__name__, path='/week', name='Omniscope')

def create_day_card(date: datetime, date_of_interest: datetime, dataset: pd.DataFrame) -> Card:
    day_of_week = date.strftime('%A')
    is_the_day = date.date() == date_of_interest.date()
    is_future = date.date() > date_of_interest.date()

    text_color = "#333333" if is_future else ("white" if is_the_day else "lightgray")
    opacity = "opacity-75" if is_future else ""
    worst_color = 'Red' if not is_future else '#333333'
    avg_color = 'White' if not is_future else '#333333'
    best_color = 'Green' if not is_future else '#333333'
    total_hours_color = 'white' if not is_future else '#333333'

    ds = dataset[dataset['Date'] == date.date()]
    total_hours = ds['TimeInHs'].sum()
    ds = dataset[dataset['Date'] != date.date()]
    ds = ds[ds['DayOfWeek'] == day_of_week]

    ds = ds.groupby('Date')['TimeInHs'].sum()

    if len(ds) > 0:
        best_day = ds.idxmax()
        best_day_hours = ds.max()

        worst_day = ds.idxmin()
        worst_day_hours = ds.min()

        average_hours = ds.mean()
    else:
        best_day = '-'
        best_day_hours = 0

        worst_day = '-'
        worst_day_hours = 0

        average_hours = 0

    return dbc.Card(
        html.A(
            [
                dbc.CardHeader(
                    [
                        html.P(day_of_week, style={'color': text_color}, className=f"fw-bold mb-1"),
                        html.Small(format_date_with_suffix(date), style={'color': text_color}, className=f"fw-bold")
                    ],
                    className="bg-light text-center p-2"
                ),
                dbc.CardBody(
                    [
                        html.H4(f'{total_hours:.1f}', style={'color': total_hours_color}, className="mb-2"),
                        c.bottom(average_hours, total_hours) if (
                                    not is_future and total_hours > 0 and average_hours > 0) else html.Div(
                            "N/A", style={'color': '#333333'}
                        ),
                    ], className="d-flex flex-column text-center p-3"
                ),
                dbc.CardFooter(
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Row(
                                    [
                                        html.Small(
                                            format_date_with_suffix(worst_day), className="text-start",
                                            style={'color': worst_color, 'font-size': '0.6rem'}
                                        ),
                                        html.Small(
                                            f'{worst_day_hours:.1f}', className="text-start",
                                            style={'color': worst_color}
                                        ),
                                    ],
                                    className="flex-column"
                                ),
                                className="text-start"
                            ),
                            dbc.Col(
                                dbc.Row(
                                    [
                                        html.Small(
                                            f'{average_hours:.1f}', style={'color': avg_color}, className="text-center"
                                        ),
                                    ],
                                    className="flex-column"
                                ),
                                className="text-center"
                            ),
                            dbc.Col(
                                dbc.Row(
                                    [
                                        html.Small(
                                            format_date_with_suffix(best_day), className="text-end",
                                            style={'color': best_color, 'font-size': '0.6rem'}
                                        ),
                                        html.Small(
                                            f'{best_day_hours:.1f}', className="text-end", style={'color': best_color}
                                        ),
                                    ],
                                    className="flex-column"
                                ),
                                className="text-end"
                            ),
                        ],
                        className="gx-2"
                    ),
                    className="bg-light text-center p-2"
                )
            ],
            href="#",
            id={'type': 'day-card', 'index': date.strftime('%Y-%m-%d')},
            className="text-decoration-none"
        ),
        className=f'h-100 shadow-sm {opacity} cursor-pointer'
    )


def create_week_row(date_of_interest: datetime, kind: str) -> html.Div:
    start_of_week, end_of_week = Weeks.get_week_dates(date_of_interest)
    week = Weeks.get_week_string(date_of_interest)

    dataset = globals.datasets.timesheets.get_last_six_weeks(date_of_interest)
    df = dataset.data
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date
    df = df[df['Kind'] == kind]

    dates = [
        start_of_week + timedelta(days=i)
        for i in range(7)
    ]

    cards = [
        create_day_card(d, date_of_interest, df)
        for d in dates
    ]

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(card, width=True)
                    for card in cards
                ], style={'marginBottom': '10px'}
            ),
            asbst.render(tsds.get_six_weeks_allocation_analysis(df, date_of_interest))
        ]
    )


def layout():
    return html.Div(
        [
            dcc.DatePickerSingle(
                id='week-datepicker',
                display_format='MMM Do, YY',
                month_format='MMM Do, YY',
                placeholder='MMM Do, YY',
                date=datetime.today().date()
            ),
            dcc.Store(id='selected-date-store'),
            html.Div(id='week-content-area')
        ]
    )


@callback(
    Output('week-content-area', 'children'),
    Input('week-datepicker', 'date'),
)
def update_week_content_area(selected_date: str):
    date_of_interest = datetime.strptime(selected_date, '%Y-%m-%d')

    return html.Div(
        [
            title.render('Squad Week', 3),
            create_week_row(date_of_interest, 'Squad'),
            title.render('Consulting Week', 3),
            create_week_row(date_of_interest, 'Consulting')
        ]
    )


@callback(
    Output('week-datepicker', 'date'),
    Input({'type': 'day-card', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State({'type': 'day-card', 'index': dash.dependencies.ALL}, 'id'),
    prevent_initial_call=True
)
def update_date_picker(n_clicks, ids):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update

    clicked_card = ast.literal_eval(ctx.triggered[0]['prop_id'].split('.')[0])
    clicked_date = datetime.strptime(clicked_card['index'], "%Y-%m-%d").date()

    if clicked_date:
        return clicked_date

    return dash.no_update
