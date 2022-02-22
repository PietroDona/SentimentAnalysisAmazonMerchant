from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots

import pandas as pd

import dash_bootstrap_components as dbc

from Dashboard.styles import TITLE_STYLE


def rating_summary(df: pd.DataFrame) -> dbc.Col:

    df_tmp = df['review_rating'].value_counts().sort_index()
    df_ratings = pd.DataFrame(
        {'Rating': df_tmp.index, 'Count': df_tmp.values})
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

    df_tmp = df['review_verified'].value_counts().sort_index()
    translate = {False: "Not Verified", True: "Verified"}
    df_tmp.index = [translate[label] for label in df_tmp.index]
    df_verified = pd.DataFrame(
        {'Verified': df_tmp.index, 'Count': df_tmp.values})

    fig_pie = px.pie(df_verified, names='Verified',
                     values='Count')

    fig_pie.update_layout(template='plotly_white',
                          margin=dict(t=0))

    pieplot = dcc.Graph(
        id='pieplot',
        figure=fig_pie
    )

    tmp_df = df.copy()
    tmp_df['review_date'] = pd.to_datetime(tmp_df['review_date'])
    df_tmp = tmp_df.groupby(pd.Grouper(key='review_date', freq='M')).count()
    monthly_df = pd.DataFrame(
        {'Date': df_tmp.index, 'Count': df_tmp.review_rating})
    # df_tmp.review_rating.cumsum()
    df_tmp = tmp_df.groupby(pd.Grouper(key='review_date', freq='M')).mean()
    rev_monthly_df = pd.DataFrame(
        {'Date': df_tmp.index, 'Mean': df_tmp.review_rating})
    # fig_time = px.line(monthly_df, x="Date", y="Count",
    #                    title='Review/Time')

    # Create figure with secondary y-axis
    fig_time = make_subplots(specs=[[{"secondary_y": True}]])

    fig_time.update_layout(template='plotly_white',
                           margin=dict(t=0))

    # Add traces
    fig_time.add_trace(
        go.Scatter(x=monthly_df["Date"],
                   y=monthly_df["Count"], name="Number of reviews"),
        #px.line(monthly_df, x="Date", y="Count"),
        secondary_y=False,
    )

    # Add traces
    fig_time.add_trace(
        go.Scatter(x=rev_monthly_df["Date"],
                   y=rev_monthly_df["Mean"], name="Average rating"),
        #px.line(rev_monthly_df, x="Date", y="Mean"),
        secondary_y=True,
    )

    fig_time.update_yaxes(
        title_text="Reviews", secondary_y=False)
    fig_time.update_yaxes(
        title_text="Rating", secondary_y=True)

    fig_time.update_xaxes(showline=True, linewidth=1,
                          linecolor='black')  # , mirror=True)
    fig_time.update_yaxes(showline=True, linewidth=1,
                          linecolor='black')  # , mirror=True)

    fig_time.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    timeplot = dcc.Graph(
        id='reviewtimeplot',
        figure=fig_time
    )

    return [
        html.H3("Reviews summary", style=TITLE_STYLE),
        dbc.Col([
            html.H5("Reviews distribution", style=TITLE_STYLE),
            countplot],
            width=3,
            id="count"
        ),
        dbc.Col([html.H5("Reviews in time", style=TITLE_STYLE),
                 timeplot],
                width=6,
                id="time"
                ),
        dbc.Col([html.H5("Reviews verified", style=TITLE_STYLE),
                 pieplot],
                width=3,
                id="helpful"
                )]
