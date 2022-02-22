from dash import dcc, html
import dash_bootstrap_components as dbc
from Dashboard.styles import TITLE_STYLE


def create_samplereviews_block() -> dbc.Col:
    return [dbc.Col([
        dbc.Col([
            html.H3("Reviews sample", style=TITLE_STYLE),
            html.H3("Placeholder", style={"height": "10rem"})],
            class_name="border rounded",
            width=12,
            id="sample"
        )],)]
