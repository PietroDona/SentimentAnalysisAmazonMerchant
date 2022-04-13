'''
Module to process the scraped data
'''

from SentimentAnalysis.aspect_clustering import extract_aspects
import ProductReviewScraper.amazon_review_database as db
from ProductReviewScraper.models import Review, Product
import pandas as pd
from pathlib import Path
import unidecode
from wordcloud import WordCloud


def my_rating_count(df):
    rating_series = df['review_rating']
    five = (rating_series == 5).sum()
    four = (rating_series == 4).sum()
    three = (rating_series == 3).sum()
    two = (rating_series == 2).sum()
    one = (rating_series == 1).sum()

    return [one, two, three, four, five]


def make_product_list():
    df = pd.read_sql(
        db.session.query(
            Product, Review).filter(Review.product_id == Product.id).statement,
        con=db.engine
    )
    product_list = df['asin'].unique()
    pd.DataFrame(product_list).to_csv(
        "data/product_list.csv", header=None, index=False)
    return product_list


def make_review_df(strasin: str):

    df = pd.read_sql(
        db.session.query(
            Product, Review).filter(Review.product_id == Product.id, Product.asin == strasin).statement,
        con=db.engine
    )

    df.drop(['id', 'id_1', 'product_id'],
            axis='columns', inplace=True)
    df.columns = ['product_asin', 'product_name',  'product_imageurl',
                  'product_price', 'product_global_rating', 'review_amazonid',
                  'review_user', 'review_rating', 'review_title',
                  'review_date', 'review_verified', 'review_foreign',
                  'review_content', 'review_helpful_vote']
    df.drop(['product_asin', 'product_name',  'product_imageurl',
             'product_price', 'product_global_rating'], axis='columns', inplace=True)

    df = df[df["review_foreign"] == False].copy()

    df.drop(["review_foreign"],
            axis='columns', inplace=True)

    df["review_content"] = df["review_content"].apply(unidecode.unidecode)
    df["review_title"] = df["review_title"].apply(unidecode.unidecode)

    product_path = Path(f"data/{strasin}")
    product_path.mkdir(exist_ok=True)
    df.to_csv(product_path / "reviews.csv", index=False)

    return df


def make_product_info_df(strasin: str):

    df = pd.read_sql(
        db.session.query(
            Product, Review).filter(Review.product_id == Product.id, Product.asin == strasin).statement,
        con=db.engine
    )

    df.drop(['id', 'id_1', 'product_id'],
            axis='columns', inplace=True)
    df.columns = ['product_asin', 'product_name',  'product_imageurl',
                  'product_price', 'product_global_rating', 'review_amazonid',
                  'review_user', 'review_rating', 'review_title',
                  'review_date', 'review_verified', 'review_foreign',
                  'review_content', 'review_helpful_vote']

    df.drop(['review_user', 'review_rating', 'review_title',
             'review_date', 'review_verified', 'review_foreign',
             'review_content', 'review_helpful_vote', 'review_amazonid'],
            axis='columns', inplace=True)

    product_df = df.head(n=1).copy()
    product_df['product_reviews_count'] = [len(df)]

    product_df["product_name"] = product_df["product_name"].apply(
        unidecode.unidecode)

    product_path = Path(f"data/{strasin}")
    product_path.mkdir(exist_ok=True)

    product_df.to_csv(product_path / "product_info.csv", index=False)


def make_weekly_summary(df, strasin):
    df['review_date'] = pd.to_datetime(df['review_date'])

    df4years = df[df['review_date'] >= "2018-1-1"]
    df_count = df4years.groupby(pd.Grouper(
        key='review_date', freq='W')).count()
    df_mean = df4years.groupby(pd.Grouper(key='review_date', freq='W')).mean()
    weekly_reviews = pd.DataFrame(
        {'Date': df_mean.index,
         'Mean': df_mean.review_rating,
         'AveragedMean': df_mean.review_rating.rolling(4, center=True).mean(),
         'Count': df_count.review_rating,
         'AveragedCount': df_count.review_rating.rolling(4, center=True).mean()
         })
    product_path = Path(f"data/{strasin}")
    weekly_reviews.to_csv(product_path / "weekly_reviews.csv", index=False)


def make_summary(df, strasin):
    df['review_date'] = pd.to_datetime(df['review_date'])
    df4years = df[df['review_date'] >= "2018-1-1"]
    df_count = df4years.groupby(pd.Grouper(
        key='review_date', freq='W')).count()

    dfrecent = df[df['review_date'] >= "2022-1-1"]
    df_ratings = pd.DataFrame(
        {'Rating': [1, 2, 3, 4, 5],
         'Count': my_rating_count(df),
         'CountRecent': my_rating_count(dfrecent),
         })
    summary_reviews = pd.DataFrame(
        {'Mean': [df.review_rating.mean()],
         'RevWeek': [df_count.review_rating.mean()],
         'Recent': [dfrecent.review_rating.mean()],
         'Verified': [df['review_verified'].sum() / len(df)]
         })
    product_path = Path(f"data/{strasin}")
    summary_reviews.to_csv(product_path / "summary_reviews.csv", index=False)

    df_ratings.to_csv(product_path / "rating_reviews.csv", index=False)


def make_word_cloud(df, strasin):
    words = list(df['review_content'])
    fulltext = " ".join(words)
    # Create the wordcloud object
    wordcloud = WordCloud(background_color=None,
                          width=480, height=360).generate(fulltext)
    wordcloud_svg = wordcloud.to_svg(embed_font=True)
    product_path = Path(f"data/{strasin}")
    filepath = product_path / "wordcloud.svg"
    with filepath.open("w", encoding="utf-8") as f:
        f.write(wordcloud_svg)


def analyse_all():
    produc_list = make_product_list()
    for product in produc_list:
        review_df = make_review_df(product)
        if len(review_df) > 2000:
            make_product_info_df(product)
            make_summary(review_df, product)
            make_weekly_summary(review_df, product)
            make_word_cloud(review_df, product)
            extract_aspects(review_df, product)


if __name__ == "__main__":
    analyse_all()
