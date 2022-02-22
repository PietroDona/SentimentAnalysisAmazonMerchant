# custom review container

from ProductReviewScraper.amazon_product_scraper import ProductDetailsScraper
from ProductReviewScraper.amazon_review_scraper import ProductReviewsScraper
import ProductReviewScraper.amazon_review_database as db
import logging


def main_scrape():
    logging.basicConfig(
        filename="scrape.log",
        filemode="w",
        format="%(asctime)s AMAZON-SCRAPER: %(message)s",
        level=logging.INFO,
    )


# "B082V6C83P", "B07QGWY83T", "B07DQWT15Y", "B08N5LFLC3", "B0831BF1FH"
    asin_list = ["B000X457HO", "B000JDGC78", "B01N0RSCBI", "B000WUFVR0"]

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
    main_scrape()
