import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc
from Dashboard.styles import TITLE_STYLE
from Dashboard import connect_to_database
from pathlib import Path
import plotly.graph_objects as go
#######################################################################
#                                LAYOUT                               #
#######################################################################

aspect_block = dbc.Row(
    [
        html.H3("Reviews content", style=TITLE_STYLE),
        dbc.Col([
            html.H5("Words in the reviews", style=TITLE_STYLE),
            dbc.Col("", id="wordcloud",
                    class_name="text-center")
        ],
            width=4
        ),
        dbc.Col([
            html.H5("Product features", style=TITLE_STYLE),
            dbc.Col("", id="clusters",
                    class_name="text-center")
        ],
            width=4
        ),
        dbc.Col([
            html.H5("Features impact", style=TITLE_STYLE),
            dbc.Col("", id="aspectanalysis")
        ],
            width=4
        ),
    ],
    id="aspectblock",
    class_name="mb-4"
)

#######################################################################
#                              FUNCTIONS                              #
#######################################################################


def make_word_cloud(strasin: str) -> dbc.Col:
    wordcloud_file = Path("data") / strasin / "wordcloud.svg"
    with wordcloud_file.open("r", encoding="utf-8") as f:
        image_svg = f.read()

    return html.Img(
        src="data:image/svg+xml;charset=utf-8, " + image_svg,
        className="img-fluid"
    ),


def row_name(aspects, sizes, color, cluster_name):
    header = [dbc.Col(
        cluster_name,
        width=12, class_name="fs-6")]

    content = [dbc.Col([a, dbc.Progress(value=s)])
               for a, s in zip(aspects, sizes)]

    return dbc.Row(header + content, class_name="border rounded p-1 mb-1")


def make_clusters(strasin: str) -> dbc.Col:
    df = connect_to_database.get_cluster_aspects_review_df(strasin)
    colors = ["#79addc", "#ffc09f", "#ffee93", "#fcf5c7", "#adf7b6"]
    cluster_name = [df[f"Name{id}"].iloc[0].title() for id in range(5)]
    return [row_name(df[f"Name{id}"], df[f"Count{id}"],
                     colors[id], cluster_name[id]) for id in range(5)]


def normalize(lista):
    s = sum(lista)
    return [round(100*x/s, 1) for x in lista]


def make_polarity(strasin: str):
    df = connect_to_database.get_aspects_review_value_df(strasin)

    colors = ['rgb(153, 213, 191)', 'rgb(207, 207, 196)', 'rgb(255, 105, 97)']

    x_data = [list(df.query(f"Cluster=={id}")[
        ["PositivePolarity", "NeutralPolarity", "NegativePolarity"]].iloc[0]) for id in range(5)]

    y_data = df['ClusterName']

    fig = go.Figure()

    for i in range(0, len(x_data[0])):
        for xd, yd in zip(x_data, y_data):
            fig.add_trace(go.Bar(
                x=[normalize(xd)[i]], y=[yd],
                orientation='h',
                marker=dict(
                    color=colors[i],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                )
            ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.15, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=30, r=30, t=30, b=0),
        showlegend=False,
        height=200,
    )

    annotations = []
    for yd, xd in zip(y_data, x_data):
        # labeling the y-axis
        annotations.append(dict(xref='paper', yref='y',
                                x=0.14, y=yd,
                                xanchor='right',
                                text=str(yd),
                                font=dict(family='Arial', size=14,
                                          color='rgb(67, 67, 67)'),
                                showarrow=False, align='right'))
        # labeling the series
        annotations.append(dict(xref='paper', yref='y',
                                x=0.96, y=yd,
                                xanchor='left',
                                text=str(sum(xd)),
                                font=dict(family='Arial', size=14,
                                          color='rgb(67, 67, 67)'),
                                showarrow=False, align='right'))
        space = 0
        for i in range(len(xd)):
            # labeling the percentages of each bar (x_axis)
            annotations.append(dict(xref='x', yref='y',
                                    x=space + normalize(xd)[i] / 2, y=yd,
                                    text=str(normalize(xd)[i]) + '%',
                                    font=dict(family='Arial', size=14,
                                              color='rgb(67, 67, 67)'),
                                    showarrow=False))

            space += normalize(xd)[i]

    labels = "Positive", "Neutral", "Negative"
    space = 0
    for i in range(len(x_data[0])):
        # labeling the percentages of each bar (x_axis)
        annotations.append(dict(xref='x', yref='paper',
                                x=space + normalize(x_data[-1])[i] / 2, y=1.15,
                                text=labels[i],
                                font=dict(family='Arial', size=16,
                                          color='rgb(67, 67, 67)'),
                                showarrow=False))

        space += normalize(x_data[-1])[i]

    annotations.append(dict(xref='paper', yref='paper',
                            x=0, y=0.5, textangle=-90,
                            text="Sentiment",
                            font=dict(family='Arial', size=20,
                                      color='rgb(67, 67, 67)'),
                            showarrow=False))
    fig.update_layout(annotations=annotations)

    return dcc.Graph(figure=fig)


def make_ratings(strasin: str):
    df = connect_to_database.get_aspects_review_value_df(strasin)

    colors = ['rgb(153, 213, 191)', 'rgb(207, 207, 196)', 'rgb(255, 105, 97)']

    x_data = [list(df.query(f"Cluster=={id}")[
        ["PositiveRating", "NeutralRating", "NegativeRating"]].iloc[0]) for id in range(5)]

    y_data = ["Scent", "Buy", "Strong", "Candle", "Burn"]

    fig = go.Figure()

    for i in range(0, len(x_data[0])):
        for xd, yd in zip(x_data, y_data):
            fig.add_trace(go.Bar(
                x=[normalize(xd)[i]], y=[yd],
                orientation='h',
                marker=dict(
                    color=colors[i],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                )
            ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.15, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=30, r=30, t=30, b=0),
        showlegend=False,
        height=200,
    )

    annotations = []
    for yd, xd in zip(y_data, x_data):
        # labeling the y-axis
        annotations.append(dict(xref='paper', yref='y',
                                x=0.14, y=yd,
                                xanchor='right',
                                text=str(yd),
                                font=dict(family='Arial', size=14,
                                          color='rgb(67, 67, 67)'),
                                showarrow=False, align='right'))
        # labeling the series
        annotations.append(dict(xref='paper', yref='y',
                                x=0.96, y=yd,
                                xanchor='left',
                                text=str(sum(xd)),
                                font=dict(family='Arial', size=14,
                                          color='rgb(67, 67, 67)'),
                                showarrow=False, align='right'))
        space = 0
        for i in range(len(xd)):
            # labeling the percentages of each bar (x_axis)
            annotations.append(dict(xref='x', yref='y',
                                    x=space + normalize(xd)[i] / 2, y=yd,
                                    text=str(normalize(xd)[i]) + '%',
                                    font=dict(family='Arial', size=14,
                                              color='rgb(67, 67, 67)'),
                                    showarrow=False))

            space += normalize(xd)[i]

    labels = "Positive", "Neutral", "Negative"
    space = 0
    for i in range(len(x_data[0])):
        # labeling the percentages of each bar (x_axis)
        annotations.append(dict(xref='x', yref='paper',
                                x=space + normalize(x_data[-1])[i] / 2, y=1.15,
                                text=labels[i],
                                font=dict(family='Arial', size=16,
                                          color='rgb(67, 67, 67)'),
                                showarrow=False))

        space += normalize(x_data[-1])[i]

    annotations.append(dict(xref='paper', yref='paper',
                            x=0, y=0.5, textangle=-90,
                            text="Rating",
                            font=dict(family='Arial', size=20,
                                      color='rgb(67, 67, 67)'),
                            showarrow=False))
    fig.update_layout(annotations=annotations)

    return dcc.Graph(figure=fig)


def make_aspect_analysis(strasin: str):
    return dbc.Row([make_polarity(strasin),
                    make_ratings(strasin)])
