from dash import Dash, html, callback_context
from dash import Input, Output, State


import dash_bootstrap_components as dbc

from Dashboard.styles import HEADER_STYLE

from Dashboard.components import search_bar
from Dashboard.components import product_title
from Dashboard.components import summary_cards
from Dashboard.components import summary_block
from Dashboard.components import aspect_block
from Dashboard.components import newproduct

# import asyncio
# import diskcache
# from dash.long_callback import DiskcacheLongCallbackManager
# cache = diskcache.Cache("./cache")
# long_callback_manager = DiskcacheLongCallbackManager(cache)

#######################################################################
#                             SEARCH  BAR                             #
#######################################################################

app = Dash(external_stylesheets=[
    dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],)
#   long_callback_manager=long_callback_manager)


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
    Input('productdropdown', 'value'),
    State('switch_monthly', 'value')
)
def populate_page(value, monthly):

    return [product_title.create_product_title(value),
            summary_cards.create_general_info_card(value),
            summary_cards.create_number_review_card(value),
            summary_cards.create_aspect_card(value),
            summary_cards.random_review(value),
            summary_block.make_count_plot(value),
            summary_block.make_time_plot_count(value, monthly),
            summary_block.make_count_plot_verified(value),
            aspect_block.make_word_cloud(value),
            aspect_block.make_clusters(value),
            aspect_block.make_aspect_analysis(value),
            ]

#######################################################################
#                             NEW PRODUCT                             #
#######################################################################


@app.callback(
    [Output("modal", "is_open"),
     Output("productinput", "value")],
    [Input("open", "n_clicks"),
     Input("close", "n_clicks"),
     Input("addproduct", "n_clicks")],
    [State("modal", "is_open"), State("productinput", "value")],
)
def toggle_modal(n1, n2, conf,  is_open, prodcutasin):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if changed_id in ["open.n_clicks", "close.n_clicks"]:
        return [not is_open, ""]
    if changed_id in ["addproduct.n_clicks"]:
        return [not is_open, ""]
    return [is_open, ""]


# @app.long_callback(
#     output=Output("placeholder", "children"),
#     #output=Output("status_success", "is_open"),
#     inputs=Input("addproduct", "n_clicks"),
#     running=[
#         (Output("status_alert", "is_open"),  True, False),
#         # (Output("status_success", "is_open"),  False, True),
#         (Output("open", "disabled"), True, False),
#     ],
#     state=State("productinput", "value")
# )
# def callback(n_clicks, asininput):
#     changed_id = [p['prop_id'] for p in callback_context.triggered][0]
#     if asininput and changed_id == 'addproduct.n_clicks':
#         asyncio.run(newproduct.download_reviews(asininput.strip()))
#         return "Banana"
#     return "Kiwi"

# B001U40C6W
# B000WQY7RO
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
        newproduct.alert_div,
        newproduct.success_div,
        product_title.product_title,
        summary_cards.cards_block,
        html.Hr(className="mt-4"),
        summary_block.summary_block,
        html.Hr(className="mt-4"),
        aspect_block.aspect_block,
        # html.Hr(className="mt-4"),
        # detailed_review_block.detailed_review_block,
    ], fluid=True
)


if __name__ == "__main__":
    app.run_server(debug=True)
