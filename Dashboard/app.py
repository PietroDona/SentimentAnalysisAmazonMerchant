from dash import Dash, dcc, html
from dash import Input, Output

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from Dashboard.styles import HEADER_STYLE, TITLE_STYLE

from Dashboard import connect_to_database
from Dashboard.components import product_title
from Dashboard.components import summary_cards
from Dashboard.components import summary_block
from Dashboard.components import wordcloud_block
from Dashboard.components import detailed_review_block

#######################################################################
#                             SEARCH  BAR                             #
#######################################################################

app = Dash(external_stylesheets=[
    dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

search_bar = [
    dbc.Col([
        dcc.Dropdown(
            connect_to_database.load_product_list(),
            'B07H256MBK',
            id='productdropdown')], width=10),
    dbc.Col([
        dbc.Button([html.I(className="bi bi-plus-lg me-2"),
                    "Add"],
                   outline=True, color="dark"),
    ], width=2, class_name="d-grid gap-2")]

#######################################################################
#                           UPDATE DASHBOARD                          #
#######################################################################


@app.callback(
    [Output('producttitle', 'children'),
     Output('card1', 'children'),
     Output('card2', 'children'),
     Output('card3', 'children'),
     Output('card4', 'children'),
     Output('summaryblock', 'children'),
     Output('wordcloudblock', 'children'),
     Output('detailsblock', 'children')],
    Input('productdropdown', 'value')
)
def populate_page(value):
    df = connect_to_database.get_reviews_dataframe(value)
    return [product_title.create_product_title(df),
            summary_cards.create_average_review_card(df),
            summary_cards.create_number_review_card(df),
            summary_cards.placeholder_card(),
            summary_cards.placeholder_card(),
            summary_block.rating_summary(df),
            wordcloud_block.create_wordcloud_block(df),
            detailed_review_block.create_samplereviews_block()]

#######################################################################
#                                LAYOUT                               #
#######################################################################


app.layout = dbc.Container(
    [
        dbc.Row(
            [html.H1("Amazon Products Review Analysis",
                     style=HEADER_STYLE), ]
        ),
        dbc.Row(
            search_bar
        ),
        dbc.Row(
            "",
            id="producttitle"
        ),
        dbc.Row(
            [
                dbc.Col("", width=3, class_name="d-grid gap-2", id="card1"),
                dbc.Col("", width=3, class_name="d-grid gap-2", id="card2"),
                dbc.Col("", width=3, class_name="d-grid gap-2", id="card3"),
                dbc.Col("", width=3, class_name="d-grid gap-2", id="card4"),
            ]
        ),
        html.Hr(className="mt-4"),
        dbc.Row(
            "",
            id="summaryblock",
            class_name="mb-4"
        ),
        dbc.Row("",
                id="wordcloudblock",
                class_name="mb-4"
                ),
        dbc.Row(
            "",
            id="detailsblock",
            class_name="mb-4"
        ),
    ], fluid=True
)


if __name__ == "__main__":
    app.run_server(debug=True)


# febd69
# 232f3e
# 37475a
# 131a22
