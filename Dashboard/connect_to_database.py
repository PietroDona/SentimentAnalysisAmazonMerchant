import pandas as pd


def load_product_list():
    df_products = pd.read_csv("data/product_list.csv", header=None)
    return list(df_products[0])


def get_reviews_df(value: str) -> pd.DataFrame:
    df_reviews = pd.read_csv(f"data/{value}/reviews.csv")
    return df_reviews


def get_product_df(value: str) -> pd.DataFrame:
    df_product = pd.read_csv(f"data/{value}/product_info.csv")
    return df_product


def get_weekly_df(value: str) -> pd.DataFrame:
    df_weekly = pd.read_csv(f"data/{value}/weekly_reviews.csv")
    return df_weekly


def get_review_summary_df(value: str) -> pd.DataFrame:
    df_summary = pd.read_csv(f"data/{value}/summary_reviews.csv")
    return df_summary
