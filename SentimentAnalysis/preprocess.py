from wordcloud import WordCloud
from ProductReviewScraper.models import Review, Product
import ProductReviewScraper.amazon_review_database as db
import pandas as pd


def load_dataframe_asin(strasin: str) -> pd.DataFrame:
    df = pd.read_sql(
        db.session.query(
            Product, Review).filter(Review.product_id == Product.id,
                                    Product.asin == strasin).statement,
        con=db.engine
    )

    df.drop(['id', 'id_1', 'product_id'],
            axis='columns', inplace=True)
    df.columns = ['product_asin', 'product_name',  'product_imageurl',
                  'product_price', 'product_max_reviews', 'review_amazonid',
                  'review_user', 'review_rating', 'review_title',
                  'review_date', 'review_verified', 'review_foreign',
                  'review_content', 'review_helpful_vote']
    df['review_helpful_vote'].fillna(0, inplace=True)

    return df


def make_wordcloud(series: pd.Series):
    text = " ".join(list(series))
    # Create the wordcloud object
    wordcloud = WordCloud(width=800, height=600).generate(text)
    return wordcloud
