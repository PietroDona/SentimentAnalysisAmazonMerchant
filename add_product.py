'''
Module to add a Product to the database and the dashboard
'''

from ProductReviews.amazon_product_scraper import ProductDetailsScraper
from ProductReviews.amazon_review_scraper import ProductReviewsScraper
import ProductReviews.amazon_review_database as db
import logging

import data_preprocess


def product_scrape():
    logging.basicConfig(
        filename="scrape.log",
        filemode="w",
        format="%(asctime)s AMAZON-SCRAPER: %(message)s",
        level=logging.INFO,
    )

    print('What product do you want to scrape?')
    strasin = input('ASIN: ')

    print('Scraping the product informations')
    try:
        aps = ProductDetailsScraper(asin=strasin)
        product = aps.get_product_info()
    except AttributeError:
        print(f"The ASIN {strasin} is not valid.")
        print(
            f"We were not able to find the product at the link https://www.amazon.com/dp/{strasin}")
        return

    print('Scraping the product reviews starting from the most recent')
    try:
        ars = ProductReviewsScraper(
            asin=strasin, sort="recent"
        )
        reviews = ars.get_reviews()
        product.reviews = reviews
        print(f"We extracted {len(reviews)} reviews.")
    except AttributeError:
        print(f"The product ASIN {strasin} has no valid reviews.")
        return

    print('Adding the data to the database.')

    db.session.add(product)
    db.session.add_all(reviews)
    db.session.commit()

    print('Do you want to process the data for the dashboard?')
    while (reply := input("(yes/no): ")) not in ['yes', 'no']:
        pass

    if reply == "yes":
        _ = data_preprocess.make_product_list()
        review_df = data_preprocess.make_review_df(strasin)
        print('Compiling product info.')
        data_preprocess.make_product_info_df(strasin)
        print('Compiling the summary info.')
        data_preprocess.make_summary(review_df, strasin)
        data_preprocess.make_weekly_summary(review_df, strasin)
        print('Making the world cloud.')
        data_preprocess.make_word_cloud(review_df, strasin)
        print('Extracting the aspects, this operation could take a few minuts.')
        data_preprocess.extract_aspects(review_df, strasin)


if __name__ == "__main__":
    product_scrape()
