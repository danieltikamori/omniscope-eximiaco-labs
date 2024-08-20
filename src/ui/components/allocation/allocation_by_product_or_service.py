from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
import ui.components.base.colors as colors
import ui.components.base.cards as c

from models.datasets.timesheet_dataset import TimeSheetFieldSummary


def render(data: pd.DataFrame):
    if len(data) == 0:
        return html.Div()

    tfs = TimeSheetFieldSummary(data, 'ProductsOrServices')
    return html.Div(
        [
            dbc.Row([
                c.create_kpi_card('Products or Services', tfs.unique, 4),
                c.create_kpi_card('Avg. Hours per POS', f'{tfs.avg_hours:.1f} hrs', 4),
                c.create_kpi_card('Std. Hours per POS', f'{tfs.std_hours:.1f}', 4),
            ], style={'marginBottom': '10px'}),
            dbc.Row(
                [
                    dbc.Col(
                        c.create_graph_card(
                            "All POS by Hours",
                            dcc.Graph(
                                figure={
                                    'data': [
                                                go.Bar(
                                                    x=tfs.grouped_total_hours.index,
                                                    y=tfs.grouped_total_hours[kind],
                                                    name=kind,
                                                    marker_color=colors.KIND_COLORS[kind]
                                                ) for kind in tfs.grouped_total_hours.columns[:-1]
                                            ] + [
                                                go.Scatter(
                                                    x=[tfs.allocation_80, tfs.allocation_80],
                                                    y=[0, tfs.grouped_total_hours['Total'].max()],
                                                    mode='lines',
                                                    name='80% Allocation',
                                                    line=dict(color='red', dash='dash')
                                                )
                                            ],
                                    'layout': go.Layout(
                                        barmode='stack',
                                        xaxis={'title': 'POS', 'tickangle': 45},
                                        yaxis={'title': 'Hours'},
                                        showlegend=True,
                                        legend={'orientation': 'h', 'y': -0.2},
                                        plot_bgcolor='rgba(0,0,0,0)',
                                        paper_bgcolor='rgba(0,0,0,0)',
                                        font_color='white',
                                        margin=dict(l=50, r=20, t=20, b=100),
                                        height=500
                                    )
                                }
                            )
                        ), width=12
                    )
                ]
            ),
        ]
    )
