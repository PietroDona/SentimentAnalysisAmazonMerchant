# custom review container
from models import Review, Product

from amazon_merchant_scraper import MerchantScraper
from amazon_review_scraper import ReviewScraper
import logging

if __name__ == "__main__":

    logging.basicConfig(filename='scrape.log', filemode='w',
                        format='%(asctime)s AMAZON-SCRAPER: %(message)s', level=logging.INFO)
    ams = MerchantScraper(me="A294P4X9EWVXLJ", max_scrape=2, verbose=True)
    list_products = ams.get_items()
    reviews = []
    for product in list_products:
        ars = ReviewScraper(asin=product.asin, sort="helpful",
                            max_scrape=2, verbose=True)
        reviews += ars.get_reviews()

    outputfile = 'result.json'
    logging.info(f"Saving the {len(reviews)} scraped reviews in {outputfile}")

    import json
    with open(outputfile, 'w') as fout:
        json.dump([r.dict() for r in reviews], fout)
