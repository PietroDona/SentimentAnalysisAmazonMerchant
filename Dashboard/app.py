'''
Main dashboard, execute to run webserver
Dashsboard developed in Dash - Plotly
The on screen component are stored in the components directory
'''

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


#######################################################################
#                             DEFINE APP                              #
#######################################################################

app = Dash(external_stylesheets=[
    dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],)

#######################################################################
#                            UPDATE LAYOUT                            #
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
    '''Populate the dashboard with the data of the product with ASIN stored in value'''

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
#                          NEW PRODUCT  MODAL                         #
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
    ], fluid=True
)


if __name__ == "__main__":
    app.run_server(debug=True)
