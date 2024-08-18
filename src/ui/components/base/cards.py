from dash import html
import dash_bootstrap_components as dbc


def create_kpi_card(title, value, width=3, color='secondary', bottom=None):
    title_class = "text-center mb-2 text-white"
    method = html.H1 if width >= 3 else html.H3
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.P(title, className=title_class),
                    method(value, className="card-text text-center")
                ] +
                ([
                     html.P(bottom, className="card-text text-center " + ("text-white" if color != 'secondary' else ""))
                 ] if bottom else []),
            ),
            color=color,
            outline=True,
            className="mb-3 h-100 shadow-sm"
        ),
        width=width
    )


def create_graph_card(title, graph):
    return dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody([graph])
        ], className="mb-4"
    )


def create_card(title, body):
    return dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody([body])
        ], className="mb-4"
    )


def get_status_indicator(value):
    if value > 0:
        return html.Span("▲", style={"color": "green"})
    elif value < 0:
        return html.Span("▼", style={"color": "red"})
    else:
        return html.Span("=", style={"color": "gray"})


def bottom(a, b):
    if (a == 0): return html.Div([])
    perc = ((b - a) / b if b > a else (a - b) / a) * 100
    r_bottom = html.Div([get_status_indicator(b - a), html.Span(f' {perc:.1f}%')])
    return r_bottom
