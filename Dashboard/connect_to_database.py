from AmazonReviewScraper.models import Review, Product, Merchant
from AmazonReviewScraper import amazon_review_database as db
import pandas as pd


def load_product_list():
    df_products = pd.read_sql_table(
        "products",
        con=db.engine
    )
    list_of_asin = list(df_products['asin'])
    return list_of_asin


def get_reviews_dataframe(value: str) -> pd.DataFrame:
    df_reviews = pd.read_sql(
        db.session.query(
            Merchant, Product, Review).filter(Review.product_id == Product.id, Product.merchant_id == Merchant.id, Product.asin == value).statement,
        con=db.engine
    ).query(f"asin == '{value}'")
    df_reviews.drop(['id', 'id_1', 'id_2', 'merchant_id', 'product_id'],
                    axis='columns', inplace=True)
    df_reviews.columns = ['merchant_token', 'merchant_name', 'product_asin', 'product_name', 'product_average_review', 'review_user', 'review_rating',
                          'review_title', 'review_date', 'review_verified', 'review_content', 'review_helpful_vote']
    return df_reviews
