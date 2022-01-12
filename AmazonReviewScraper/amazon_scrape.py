# custom review container
from models import Review, Product, Merchant

from amazon_merchant_scraper import MerchantItemsScraper
from amazon_review_scraper import ProductReviewScraper
import logging


def ScrapeMerchant(me: str) -> None:
    ams = MerchantItemsScraper(me=me, max_scrape=2, verbose=True)
    list_products = ams.get_items()
    reviews = []
    for product in list_products:
        ars = ProductReviewScraper(asin=product.asin, sort="helpful",
                                   max_scrape=2, verbose=True)
        reviews += ars.get_reviews()

    outputfile = 'result.json'
    logging.info(f"Saving the {len(reviews)} scraped reviews in {outputfile}")

    import json
    with open(outputfile, 'w') as fout:
        json.dump([r.dict() for r in reviews], fout)


if __name__ == "__main__":
    logging.basicConfig(filename='scrape.log', filemode='w',
                        format='%(asctime)s AMAZON-SCRAPER: %(message)s',
                        level=logging.INFO)
    ScrapeMerchant("A294P4X9EWVXLJ")
