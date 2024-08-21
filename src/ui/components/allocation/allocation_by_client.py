from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
import ui.components.base.cards as c
import ui.components.base.colors as colors

from models.datasets.timesheet_dataset import TimeSheetFieldSummary

def render(data: pd.DataFrame):
    if len(data) == 0:
        return html.Div()

    tfs = TimeSheetFieldSummary(data, 'ClientName')

    columns = ['Squad', 'Consulting', 'Internal']

    return html.Div(
        [
            dbc.Row([
                c.create_kpi_card('Unique Clients', tfs.unique, 4),
                c.create_kpi_card('Avg. Hours per Client', f'{tfs.avg_hours:.1f} hrs', 4),
                c.create_kpi_card('Std. Hours per Client', f'{tfs.std_hours:.1f}', 4),
            ], style={'marginBottom': '10px'}),
            dbc.Row(
                [
                    dbc.Col(
                        c.create_graph_card(
                            "Hours Allocated by Client and Work Type",
                            dcc.Graph(
                                figure={
                                    'data': [
                                                go.Bar(
                                                    x=tfs.grouped_total_hours.index,
                                                    y=tfs.grouped_total_hours[kind],
                                                    name=kind,
                                                    marker_color=colors.KIND_COLORS[kind]
                                                ) for kind in columns if kind in tfs.grouped_total_hours
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
                                        xaxis={'title': 'Clients'},
                                        yaxis={'title': 'Hours Worked'},
                                        showlegend=True,
                                        legend={'orientation': 'h', 'y': -0.2},
                                        plot_bgcolor='rgba(0,0,0,0)',
                                        paper_bgcolor='rgba(0,0,0,0)',
                                        font_color='white',
                                        margin=dict(l=50, r=20, t=20, b=100),
                                        height=400
                                    )
                                }
                            )
                        ), width=12
                    )
                ]
            )
        ]
    )
