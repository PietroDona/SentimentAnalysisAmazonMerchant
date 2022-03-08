import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc
from Dashboard.styles import TITLE_STYLE

#######################################################################
#                                LAYOUT                               #
#######################################################################

detailed_review_block = dbc.Row(
    [
        html.H3("Detailed reviews content", style=TITLE_STYLE),
        dbc.Col([
            html.H5("Column 1", style=TITLE_STYLE),
            dbc.Col("", id="col1")
        ],
            width=3
        ),
        dbc.Col([
            html.H5("Review Details", style=TITLE_STYLE),
            dbc.Col("", id="col2")
        ],
            width=6
        ),
        dbc.Col([
            html.H5("Column 2", style=TITLE_STYLE),
            dbc.Col("", id="col3")
        ],
            width=3
        ),
    ],
    id="details_review",
    class_name="mb-4"
)

#######################################################################
#                              FUNCTIONS                              #
#######################################################################
