from dash import html
import dash_bootstrap_components as dbc


def create_card(title: str, body: str, link: str) -> dbc.Card:
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4(title, className="card-title"),
                    html.P(
                        body,
                        className="card-text fs-2",
                    ),
                    html.A("Details", href=link)
                ]
            ),
        ],
    )


def create_average_review_card(df):
    average_review_score = ["-", html.I(className="bi bi-star-fill ms-2")]
    if not df.empty:
        score = df["product_average_review"].iloc[0]
        average_review_score = [f"{score}/5",
                                html.I(className="bi bi-star-fill ms-2")]

    return create_card(title="Average Review Score", body=average_review_score, link="#")


def create_number_review_card(df):
    number_review_score = "-"
    if not df.empty:
        number_review_score = len(df)

    return create_card(title="Number of Reviews", body=number_review_score, link="#")


def placeholder_card():
    title = "Placeholder Card"
    body = "Some quick example text."

    return create_card(title=title, body=body, link="#")
