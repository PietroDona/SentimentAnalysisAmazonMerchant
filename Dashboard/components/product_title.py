from dash import html
from Dashboard.styles import TITLE_STYLE


def create_product_title(df):
    if df.empty:
        return [html.H3("Product Name", style=TITLE_STYLE)]
    title = df["product_name"].iloc[0]
    return [html.H3(title, style=TITLE_STYLE)]
