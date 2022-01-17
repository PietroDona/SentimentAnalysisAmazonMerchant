# custom review container
from AmazonReviewScraper.models import Review, Product, Merchant

from AmazonReviewScraper.amazon_merchant_scraper import MerchantItemsScraper
from AmazonReviewScraper.amazon_review_scraper import ProductReviewScraper
import AmazonReviewScraper.amazon_review_database as db
import logging


if __name__ == "__main__":
    logging.basicConfig(filename='scrape.log', filemode='w',
                        format='%(asctime)s AMAZON-SCRAPER: %(message)s',
                        level=logging.INFO)
    anker = Merchant(me="A294P4X9EWVXLJ", name="Anker")
    db.session.add(anker)
    db.session.commit()

    ams = MerchantItemsScraper(me=anker.me, max_scrape=5, verbose=True)
    products_list = ams.get_items()
    db.session.add_all(products_list)
    db.session.commit()

    anker.products = products_list
    for product in products_list:
        ars = ProductReviewScraper(
            asin=product.asin, sort="helpful", verbose=True)
        reviews = ars.get_reviews()
        product.reviews = reviews
        db.session.add_all(reviews)
        db.session.commit()
