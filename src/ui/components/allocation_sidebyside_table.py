from dash import html
import pandas as pd
import dash_bootstrap_components as dbc

from ui.helpers.beaulty import beautify
import ui.components.base.cards as c


def render(data: pd.DataFrame):
    if len(data) == 0:
        return html.Div()

    data['Status'] = data['Status'].apply(c.get_status_indicator)
    table_header = [
        html.Thead(html.Tr([html.Th(col) for col in data.columns] + [html.Th('Diff')]))
    ]

    right_column = data.columns[-1]
    left_column = data.columns[-2]

    rows = []
    for i in range(len(data)):
        style = {}
        if data.iloc[i][left_column] == 0:
            style = {"color": "green"}
        elif data.iloc[i][right_column] == 0:
            style = {"color": "red"}

        rows.append(
            html.Tr(
                [
                    html.Td(beautify(data.iloc[i][col]), style=style) for col in data.columns
                ] +
                [
                    html.Td(
                        (
                            c.bottom(data.iloc[i][left_column], data.iloc[i][right_column])
                            if data.iloc[i][right_column] > 0 else ""
                        ), style=style
                    )
                ]
            )
        )

    table_body = [
        html.Tbody(
            rows
        )
    ]

    return dbc.Table(table_header + table_body, bordered=True, hover=True, responsive=True)
