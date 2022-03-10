
from dash import dcc, html

import dash_bootstrap_components as dbc

from Dashboard import connect_to_database

from Dashboard.components import newproduct
#######################################################################
#                                LAYOUT                               #
#######################################################################


search_bar = dbc.Row([
    dbc.Col([
        dcc.Dropdown(
            connect_to_database.load_product_list(),
            connect_to_database.load_product_list()[0],
            id='productdropdown')], width=10),
    dbc.Col([newproduct.new_product_modal])])
