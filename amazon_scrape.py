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

    asin_list = ["B000X457HO", "B000WQY7RO", "B000WUFVR0", "B004G9C0SQ", "B000JDGC78", "B001L2MD2E", "B001U40C6W",
                 "B000W3V8S8"]
    missing_asin = ["B000TVJ6XW", "B000P6THK8",
                    "B006QOK0ZY", "B07144XJDK", "B06X6H95GW", "B0002PW0WO"]

    for strasin in missing_asin:
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
