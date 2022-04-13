'''
Module to scrape the products and reviews of a selected sample set
"B000WQY7RO", "B001U40C6W", "B09LD7WRVS", "B06XF2TR11", "B010OYASRG"
of randomly selected products from different categories
'''

from ProductReviewScraper.amazon_product_scraper import ProductDetailsScraper
from ProductReviewScraper.amazon_review_scraper import ProductReviewsScraper
import ProductReviewScraper.amazon_review_database as db
import logging


def example_scrape():
    logging.basicConfig(
        filename="scrape.log",
        filemode="w",
        format="%(asctime)s AMAZON-SCRAPER: %(message)s",
        level=logging.INFO,
    )

    asin_list = ["B000WQY7RO", "B001U40C6W",
                 "B09LD7WRVS", "B06XF2TR11", "B010OYASRG"]

    for strasin in asin_list:
        aps = ProductDetailsScraper(asin=strasin)
        product = aps.get_product_info()

        ars = ProductReviewsScraper(
            asin=product.asin, sort="recent"
        )
        reviews = ars.get_reviews()

        missing_review = [r for r in reviews if r not in product.reviews]
        product.reviews += missing_review

        db.session.add(product)
        db.session.add_all(reviews)
        db.session.commit()


if __name__ == "__main__":
    example_scrape()
