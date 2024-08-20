from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
import ui.components.base.cards as c
import ui.components.base.colors as colors


def render(data: pd.DataFrame):
    if len(data) == 0:
        return html.Div()

    total_hours_by_client = data.groupby(['ClientName', 'Kind'])['TimeInHs'].sum().unstack().fillna(0)
    total_hours_by_client['Total'] = total_hours_by_client.sum(axis=1)
    total_hours_by_client = total_hours_by_client.sort_values('Total', ascending=False)

    # Calculate 80% allocation line
    total_hours = data['TimeInHs'].sum()
    std_hours = data.groupby(['ClientName'])['TimeInHs'].sum().std()

    cumulative_hours = total_hours_by_client['Total'].cumsum()

    unique_clients = data['ClientName'].nunique()
    cumulative_hours_80 = cumulative_hours[cumulative_hours <= cumulative_hours.iloc[-1] * 0.80]
    if len(cumulative_hours_80) == 0:
        allocation_80 = 0
    else:
        allocation_80 = cumulative_hours[cumulative_hours <= cumulative_hours.iloc[-1] * 0.80].index[-1]

    unique_clients = data['ClientName'].nunique()
    columns = ['Squad', 'Consulting', 'Internal']

    return html.Div(
        [
            dbc.Row([
                c.create_kpi_card('Unique Clients', unique_clients, 4),
                c.create_kpi_card('Avg. Hours per Client', f'{total_hours/unique_clients:.1f} hrs', 4),
                c.create_kpi_card('Std. Hours per Client', f'{std_hours:.1f}', 4),
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
                                                    x=total_hours_by_client.index,
                                                    y=total_hours_by_client[kind],
                                                    name=kind,
                                                    marker_color=colors.KIND_COLORS[kind]
                                                ) for kind in columns if kind in total_hours_by_client
                                            ] + [
                                                go.Scatter(
                                                    x=[allocation_80, allocation_80],
                                                    y=[0, total_hours_by_client['Total'].max()],
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
