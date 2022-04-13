'''
Component that summarize the informations about the product ratings
left panel - count_plot - Count plot of the ratings
center panel - time_plot - Evolution in time of the rating sampled weekly or monthly
right panel - right_plot - Count plot of the ratings from January 2022
'''

from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc

from Dashboard.styles import TITLE_STYLE
from Dashboard import connect_to_database


#######################################################################
#                                LAYOUT                               #
#######################################################################

summary_block = dbc.Row(
    [
        html.H3("Reviews summary", style=TITLE_STYLE),
        dbc.Col([
            html.H5("Ratings (all time)", style=TITLE_STYLE),
            dbc.Col("", id="count_plot")
        ],
            width=3
        ),
        dbc.Col([
            html.H5("Reviews in time", style=TITLE_STYLE),
            dbc.Checklist(
                options=[
                    {"label": "Monthly Average", "value": 0},
                ],
                value=[],
                id="switch_monthly",
                switch=True,
                style={"position": "absolute",
                       "top": "1em",
                       "right": "1em"
                       }
            ),
            html.Div("", id="time_plot")],
            width=6,
            id="time",
            style={"position": "relative"}
        ),
        dbc.Col([
            html.H5("Ratings (rencent, 2022)", style=TITLE_STYLE),
            html.Div("", id="right_plot")],
            width=3,
            id="helpful"
        )
    ],
    id="summaryblock",
    class_name="mb-4"
)


#######################################################################
#                              FUNCTIONS                              #
#######################################################################


def make_count_plot(strasin: str) -> dcc.Graph:
    df_ratings = connect_to_database.get_rating_df(strasin)

    fig_bar = px.bar(df_ratings, x='Rating', y='Count',
                     barmode='group')  # , height=400)

    fig_bar.update_layout(template='plotly_white',
                          margin=dict(t=0))
    fig_bar.update_xaxes(tickvals=[1, 2, 3, 4, 5])
    fig_bar.update_xaxes(showline=True, linewidth=1,
                         linecolor='black')
    fig_bar.update_yaxes(showline=True, linewidth=1,
                         linecolor='black')

    countplot = dcc.Graph(
        id='countplot',
        figure=fig_bar
    )

    return countplot


def make_count_plot_verified(strasin: str) -> dcc.Graph:
    df_ratings = connect_to_database.get_rating_df(strasin)

    fig_bar = px.bar(df_ratings, x='Rating', y='CountRecent',
                     barmode='group')  # , height=400)

    fig_bar.update_layout(template='plotly_white',
                          margin=dict(t=0))
    fig_bar.update_xaxes(tickvals=[1, 2, 3, 4, 5])
    fig_bar.update_xaxes(showline=True, linewidth=1,
                         linecolor='black')
    fig_bar.update_yaxes(showline=True, linewidth=1,
                         linecolor='black')

    countplot = dcc.Graph(
        id='countplot',
        figure=fig_bar
    )

    return countplot


def make_time_plot_count(strasin: str, monthly: list) -> dcc.Graph:
    # Create figure with secondary y-axis
    weekly_df = connect_to_database.get_weekly_df(strasin)

    fig_time = make_subplots(rows=2, cols=1,
                             shared_xaxes=True,
                             vertical_spacing=0.02)
    fig_time.update_layout(template='plotly_white',
                           margin=dict(t=0), showlegend=False)

    if monthly:
        average = "Averaged"
    else:
        average = ""

    fig_time.add_trace(go.Scatter(x=weekly_df["Date"],
                                  y=weekly_df[average+"Count"],
                                  name="Number of reviews"),
                       row=1, col=1)
    fig_time.add_trace(go.Scatter(x=weekly_df["Date"],
                                  y=weekly_df[average+"Mean"],
                                  name="Average Rating"),
                       row=2, col=1)

    fig_time.update_yaxes(title_text="Number of Reviews", row=1, col=1)
    fig_time.update_yaxes(title_text="Average Rating", row=2, col=1)

    fig_time.update_xaxes(showline=True, linewidth=1,
                          linecolor='black')  # , mirror=True)
    fig_time.update_yaxes(showline=True, linewidth=1,
                          linecolor='black')  # , mirror=True)

    timeplot = dcc.Graph(
        id='reviewtimeplot',
        figure=fig_time,
        # height="50%"
    )

    return timeplot
