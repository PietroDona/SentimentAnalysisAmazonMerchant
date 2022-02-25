from wordcloud import WordCloud
from ProductReviewScraper.models import Review, Product
import ProductReviewScraper.amazon_review_database as db
import pandas as pd
from pathlib import Path

DATA_PATH = Path("data")


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
                  'product_price', 'product_global_rating', 'review_amazonid',
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


def make_dir(strasin: str) -> Path:
    p = DATA_PATH / strasin
    p.mkdir(parents=True, exist_ok=True)
    return p


def make_productlist() -> None:
    df = pd.read_sql_table("products", con=db.engine)
    asin_list = df['asin']
    asin_list.to_csv(DATA_PATH / "product_list.csv", header=False, index=False)


def make_dataset(df) -> None:
    path = make_dir(df["product_asin"].iloc[0])
    df.to_csv(path / "product.csv", index=False)


def load_product_list():
    df_products = pd.read_csv("data/product_list.csv", header=None)
    return list(df_products[0])


def make_datasets() -> None:
    asin_list = load_product_list()
    for asin in asin_list:
        df = load_dataframe_asin(asin)
        make_dataset(df)
