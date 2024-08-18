import dash
from dash import html
import dash_bootstrap_components as dbc
import ui.components.tile as tile
import ui.components.base.title as title

dash.register_page(__name__, path_template="/", title='Omniscope')

# Dados dos tiles
areas_of_interest_tiles = [
    ("Side-by-side", "fas fa-columns", "/side-by-side"),
    ("Allocation", "fas fa-tasks", "/allocation"),
    ("Sales Funnel B2B", "fas fa-chart-line", "/sales-funnel-b2b"),
    ("Late Timesheet Entries", "fas fa-clock", "/lte"),
    ("Ontology Publications", "fas fa-book", "/ontology-publications"),
    ("Insights Publications", "fas fa-lightbulb", "/insights-publications"),
]

about_us_tiles = [
    ("Consultants & Engineers", "fas fa-user-tie", "/consultants"),
    ("Account Managers", "fas fa-briefcase", "/account-managers"),
    ("Clients", "fas fa-users", "/clients"),
    ("Sponsors", "fas fa-handshake", "/sponsors"),
    ("Cases", "fas fa-folder-open", "/cases"),
    ("Projects", "fas fa-project-diagram", "/projects"),
]

administrative_tools_tiles = [
    ("Datasets", "fas fa-database", "/datasets"),
    ("Inconsistency Finder", "fas fa-search", "/inconsistency-finder"),
    ("Refresh data", "fas fa-sync-alt", "/hit-refresh"),
]


# Função de layout principal
def layout():
    return html.Div(
        [
            # Seção Áreas de Interesse
            dbc.Container(
                [
                    title.render('Our Areas of Interest', level=3),
                    tile.render_row(areas_of_interest_tiles),
                ],
                className="mb-5"
            ),

            # Seção Sobre Nós
            dbc.Container(
                [
                    title.render('More About Us', level=3),
                    tile.render_row(about_us_tiles),
                ],
                className="mb-5"
            ),

            # Seção Ferramentas Administrativas
            dbc.Container(
                [
                    title.render('Administrative Tools', level=3),
                    tile.render_row(administrative_tools_tiles),
                ]
            ),
        ],
        style={'background-color': 'var(--bs-body-bg)', 'padding': '20px'}
    )
