import pandas as pd


def load_product_list():
    df_products = pd.read_csv("data/product_list.csv", header=None)
    return list(df_products[0])


def get_reviews_dataframe(value: str) -> pd.DataFrame:
    df_reviews = pd.read_csv(f"data/{value}/product.csv")
    return df_reviews
