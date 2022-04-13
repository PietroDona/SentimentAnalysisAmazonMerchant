'''
Component details for the new product modal.
Not yet implemented
'''
import dash_bootstrap_components as dbc
from dash import html

alert_div = dbc.Alert([dbc.Spinner(), "Loading, please wait ... "],
                      id="status_alert",
                      is_open=False,
                      color="warning")

success_div = dbc.Alert("Success! Reload the page to find your product in the list!",
                        id="status_success",
                        is_open=False,
                        dismissable=True,
                        color="success")

new_product_modal = html.Div(
    [
        dbc.Button([html.I(className="bi bi-plus-lg me-2"),
                    "Add"],
                   outline=True,
                   color="dark",
                   id="open",
                   class_name="w-100",
                   n_clicks=0),
        html.P(id='placeholder', hidden=True),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Add a new product")),
                dbc.ModalBody([
                    dbc.Input(
                        id="productinput", placeholder="Product ASIN to analyze", type="text"),
                    dbc.Col("It can take a while", class_name="mt-2"),
                    dbc.Col("NOT YET IMPLEMENTED",
                            class_name="mt-2 text-danger text-center"),
                    dbc.Col("Please execute the script add_product.py in the source directory to add a new product", class_name="mt-2 text-danger"), ]
                ),
                dbc.ModalFooter(
                    [dbc.Col(dbc.Button("Add product", id="addproduct", class_name="w-100", n_clicks=0)),
                     dbc.Col(dbc.Button("Close", id="close", class_name="w-100", n_clicks=0))]
                ),
            ],
            id="modal",
            is_open=False,
        ),
    ], className="w-100"
)
