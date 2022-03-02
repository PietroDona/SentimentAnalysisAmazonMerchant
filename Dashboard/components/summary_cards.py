from dash import html, dcc
import dash_bootstrap_components as dbc

from Dashboard import connect_to_database


#######################################################################
#                                LAYOUT                               #
#######################################################################

cards_block = dbc.Row(
    [
        dbc.Col("", width=3, class_name="d-grid gap-2", id="card1"),
        dbc.Col("", width=3, class_name="d-grid gap-2", id="card2"),
        dbc.Col("", width=3, class_name="d-grid gap-2", id="card3"),
        dbc.Col("", width=3, class_name="d-grid gap-2", id="card4"),
    ]
)


#######################################################################
#                              FUNCTIONS                              #
#######################################################################


def create_general_info_card(value):
    df_product = connect_to_database.get_product_df(value)
    product_global_rating = df_product["product_global_rating"].iloc[0]
    product_imageurl = df_product["product_imageurl"].iloc[0]
    product_price = df_product["product_price"].iloc[0]
    product_asin = df_product["product_asin"].iloc[0]
    product_reviews_count = df_product["product_reviews_count"].iloc[0]
    return dbc.Card(
        dbc.Row(
            [
                dbc.Col([
                    dbc.CardImg(
                        src=product_imageurl,
                        className="img-fluid rounded-start",
                        style={"aspect-ratio": "1",
                               "object-fit": "contain"
                               }
                    ),
                ], width=4, class_name="d-flex flex-wrap align-items-center"),
                dbc.Col([
                    dbc.CardBody([
                        html.P(f"Reviews scraped: {product_reviews_count}",
                               className="card-text fs-5",
                               ),
                        html.P(
                            f"Price: {product_price} $",
                            className="card-text fs-5",
                        ),
                        html.P(
                            f"Global rating: {product_global_rating}",
                            className="card-text fs-5",
                        ),
                        html.A(
                            "Go-to the product page",
                            href=f"https://www.amazon.com/dp/{product_asin}",
                            target="_blank",
                            className="btn btn-outline-primary w-100")
                    ]),
                ], width=8
                )]
        )
    )


def create_number_review_card(value):
    df_summary = connect_to_database.get_review_summary_df(value)
    review_mean = round(df_summary["Mean"].iloc[0], 2)
    review_week = int(round(df_summary["RevWeek"].iloc[0], 0))
    review_rencent = round(df_summary["Recent"].iloc[0], 2)
    review_verified = round(100*df_summary["Verified"].iloc[0], 1)

    trendcolor = "text-success" if review_rencent > review_mean else "text-danger"
    trendicon = "bi-arrow-up" if review_rencent > review_mean else "bi-arrow-down"
    return dbc.Card(
        dbc.Row(
            [
                dbc.Col([dbc.CardBody([
                    html.P(review_mean,
                           className="card-text fs-1 rounded-circle px-2 py-3",
                           style={"background-color": "#febd69",
                                  "aspect-ratio": "1"},
                           ),
                    html.P("average rating",
                           className="card-text fs-6 text-center",
                           )])

                         ], width=4),
                dbc.Col([
                    dbc.CardBody([
                        html.P(f"Weekly Reviews: {review_week}",
                               className="card-text fs-5",
                               ),
                        html.P([html.Span("Recent rating: "),
                                html.Span(review_rencent,
                                          className=trendcolor),
                                html.I(className=f"bi {trendicon} {trendcolor}")],
                               className="card-text fs-5",
                               ),
                        html.P([html.Span("Verified reviews: "),
                                html.Span(review_verified),
                                html.Span("%")
                                ],
                               className="card-text fs-5",
                               ),
                        html.A(
                            "More details", href="#summaryblock", className="btn btn-outline-primary w-100")
                    ]),
                ], width=8
                )]
        )
    )


def placeholder_card():
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.P("Placeholder Card",
                           className="card-text fs-5",
                           ),

                ]
            ),
        ],
    )
