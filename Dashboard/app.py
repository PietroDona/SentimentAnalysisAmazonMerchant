from dash import Dash, dcc, html
from dash import Input, Output

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from Dashboard.styles import HEADER_STYLE, TITLE_STYLE

from Dashboard.components import search_bar
from Dashboard.components import product_title
from Dashboard.components import summary_cards
from Dashboard.components import summary_block
from Dashboard.components import aspect_block
from Dashboard.components import detailed_review_block

#######################################################################
#                             SEARCH  BAR                             #
#######################################################################

app = Dash(external_stylesheets=[
    dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])


#######################################################################
#                           UPDATE DASHBOARD                          #
#######################################################################


@app.callback(
    [Output('producttitle', 'children'),
     Output('card1', 'children'),
     Output('card2', 'children'),
     Output('card3', 'children'),
     Output('card4', 'children'),
     Output('count_plot', 'children'),
     Output('time_plot', 'children'),
     Output('right_plot', 'children'),
     Output('wordcloud', 'children'),
     Output('clusters', 'children'),
     Output('aspectanalysis', 'children'),
     ],
    Input('productdropdown', 'value')
)
def populate_page(value):

    return [product_title.create_product_title(value),
            summary_cards.create_general_info_card(value),
            summary_cards.create_number_review_card(value),
            summary_cards.create_aspect_card(value),
            summary_cards.placeholder_card(),
            summary_block.make_count_plot(value),
            summary_block.make_time_plot_count(value),
            summary_block.make_count_plot_verified(value),
            aspect_block.make_word_cloud(value),
            aspect_block.make_clusters(value),
            aspect_block.make_aspect_analysis(value),
            ]


#######################################################################
#                                LAYOUT                               #
#######################################################################

app.layout = dbc.Container(
    [
        dbc.Row(
            [html.H1("Amazon Products Review Analysis",
                     style=HEADER_STYLE), ]
        ),
        search_bar.search_bar,
        product_title.product_title,
        summary_cards.cards_block,
        html.Hr(className="mt-4"),
        summary_block.summary_block,
        html.Hr(className="mt-4"),
        aspect_block.aspect_block,
        html.Hr(className="mt-4"),
        detailed_review_block.detailed_review_block,
    ], fluid=True
)


if __name__ == "__main__":
    app.run_server(debug=True)


# febd69
# 232f3e
# 37475a
# 131a22
