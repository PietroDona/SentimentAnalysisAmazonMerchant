'''
Hearder component with the name of the product
'''

from dash import html
import dash_bootstrap_components as dbc

from Dashboard.styles import TITLE_STYLE
from Dashboard import connect_to_database

product_title = dbc.Row(
    "",
    id="producttitle"
)


def create_product_title(value):
    df_product = connect_to_database.get_product_df(value)
    title = df_product["product_name"].iloc[0]
    return [html.H3(title, style=TITLE_STYLE)]
