import pandas as pd
import plotly.express as px
from dash import dcc, html
import dash_bootstrap_components as dbc
from Dashboard.styles import TITLE_STYLE

from wordcloud import WordCloud


# def create_wordcloud_block() -> dbc.Col:
#     return [dbc.Col([
#         dbc.Col([
#             html.H3("Wordcloud", style=TITLE_STYLE),
#             html.H3("Placeholder", style={"height": "10rem"})],
#             class_name="border rounded",
#             width=12
#         )],)]

def make_word_cloud(df):
    negativewords = list(df.query("review_rating<3")['review_content'])
    negativetext = " ".join(negativewords)
    # Create the wordcloud object
    wordcloud = WordCloud(background_color='white',
                          width=480, height=360).generate(negativetext)
    wordcloud.to_image().save("wordcloud.PNG", format='PNG')
    wordcloud_img = html.Img(src="test.PNG")
    return wordcloud_img


def create_wordcloud_block(df: pd.DataFrame) -> dbc.Col:
    return [
        html.H3("Product features", style=TITLE_STYLE)]

# def create_wordcloud_block(df: pd.DataFrame) -> dbc.Col:
#     return [
#         html.H3("Product features", style=TITLE_STYLE),
#         dbc.Col([
#             html.H5("Wordcloud", style=TITLE_STYLE),
#             make_word_cloud(df)],
#             width=6,
#             id="count",
#             class_name="border"
#         ),
#         dbc.Col([
#             html.H5("Placeholder", style=TITLE_STYLE)],
#             width=6,
#             id="time",
#             class_name="border"
#         )]
