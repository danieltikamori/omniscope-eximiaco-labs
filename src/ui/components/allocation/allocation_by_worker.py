from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
import ui.components.base.colors as colors
import ui.components.base.cards as c


def render(data: pd.DataFrame):
    if len(data) == 0:
        return html.Div()

    # Calculate total hours by worker and kind
    total_hours = data['TimeInHs'].sum()
    total_hours_worker = data.groupby(['WorkerName', 'Kind'])['TimeInHs'].sum().unstack().fillna(0)
    total_hours_worker['Total'] = total_hours_worker.sum(axis=1)
    total_hours_worker = total_hours_worker.sort_values('Total', ascending=False)

    # Calculate 80% allocation line for workers
    cumulative_hours_worker = total_hours_worker['Total'].cumsum()
    # worker_allocation_80 = \
    #     cumulative_hours_worker[cumulative_hours_worker <= cumulative_hours_worker.iloc[-1] * 0.80].index[-1]
    std_hours = data.groupby(['WorkerName'])['TimeInHs'].sum().std()

    unique_workers = data['WorkerName'].nunique()

    cumulative_hours_80 = cumulative_hours_worker[cumulative_hours_worker <= cumulative_hours_worker.iloc[-1] * 0.80]
    if len(cumulative_hours_80) == 0:
        worker_allocation_80 = 0
    else:
        worker_allocation_80 = cumulative_hours_worker[cumulative_hours_worker <= cumulative_hours_worker.iloc[-1] * 0.80].index[-1]

    return html.Div(
        [
            dbc.Row([
                c.create_kpi_card('Unique Workers', unique_workers, 4),
                c.create_kpi_card('Avg. Hours per Worker', f'{total_hours/unique_workers:.1f} hrs', 4),
                c.create_kpi_card('Std. Hours per Worker', f'{std_hours:.1f}', 4),
            ], style={'marginBottom': '10px'}),
            dbc.Row(
                [
                    dbc.Col(
                        c.create_graph_card(
                            "All Workers by Hours",
                            dcc.Graph(
                                figure={
                                    'data': [
                                                go.Bar(
                                                    x=total_hours_worker.index,
                                                    y=total_hours_worker[kind],
                                                    name=kind,
                                                    marker_color=colors.KIND_COLORS[kind]
                                                ) for kind in total_hours_worker.columns[:-1]
                                            ] + [
                                                go.Scatter(
                                                    x=[worker_allocation_80, worker_allocation_80],
                                                    y=[0, total_hours_worker['Total'].max()],
                                                    mode='lines',
                                                    name='80% Allocation',
                                                    line=dict(color='red', dash='dash')
                                                )
                                            ],
                                    'layout': go.Layout(
                                        barmode='stack',
                                        xaxis={'title': 'Workers', 'tickangle': 45},
                                        yaxis={'title': 'Hours Worked'},
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
