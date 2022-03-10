
import dash_bootstrap_components as dbc
from dash import html

# from ProductReviewScraper.amazon_product_scraper import ProductDetailsScraper
# from ProductReviewScraper.amazon_review_scraper import ProductReviewsScraper
# import ProductReviewScraper.amazon_review_database as db
# import tmp_data_preprocess
# import logging

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
                    #html.Div("Add the ASIN of the product you want to analyze:"),
                    dbc.Input(
                        id="productinput", placeholder="Product ASIN to analyze", type="text"),
                    dbc.Col("It can take a while", class_name="mt-2"), ]
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


# async def download_reviews(strasin):
#     print("Download reviews")
#     logging.basicConfig(
#         filename="scrape.log",
#         filemode="w",
#         format="%(asctime)s AMAZON-SCRAPER: %(message)s",
#         level=logging.INFO,
#     )

#     aps = ProductDetailsScraper(asin=strasin)
#     product = aps.get_product_info()

#     ars = ProductReviewsScraper(
#         asin=product.asin, sort="recent"
#     )
#     reviews = ars.get_reviews()

#     missing_review = [r for r in reviews if r not in product.reviews]
#     product.reviews += missing_review

#     db.session.add(product)
#     db.session.add_all(reviews)
#     db.session.commit()


# def preprocess_data(product):
#     review_df = tmp_data_preprocess.make_review_df(product)
#     if len(review_df) > 2000:
#         tmp_data_preprocess.make_product_info_df(product)
#         tmp_data_preprocess.make_summary(review_df, product)
#         tmp_data_preprocess.make_weekly_summary(review_df, product)
#         tmp_data_preprocess.make_word_cloud(review_df, product)
#         tmp_data_preprocess.extract_aspects(review_df, product)
