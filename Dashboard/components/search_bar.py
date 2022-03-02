
from dash import dcc, html

import dash_bootstrap_components as dbc

from Dashboard import connect_to_database

#######################################################################
#                                LAYOUT                               #
#######################################################################


search_bar = dbc.Row([
    dbc.Col([
        dcc.Dropdown(
            connect_to_database.load_product_list(),
            connect_to_database.load_product_list()[0],
            id='productdropdown')], width=10),
    dbc.Col([
        dbc.Button([html.I(className="bi bi-plus-lg me-2"),
                    "Add"],
                   outline=True, color="dark"),
    ], width=2, class_name="d-grid gap-2")])
