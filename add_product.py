''' 
Module to add a single Product to the database and the dashboard
'''


from urllib import response
from ProductReviewScraper.amazon_product_scraper import ProductDetailsScraper
from ProductReviewScraper.amazon_review_scraper import ProductReviewsScraper
import ProductReviewScraper.amazon_review_database as db
import logging


def product_scrape():
    # logging.basicConfig(
    #     filename="scrape.log",
    #     filemode="w",
    #     format="%(asctime)s AMAZON-SCRAPER: %(message)s",
    #     level=logging.INFO,
    # )

    print('What product do you want to scrape?')
    strasin = input('ASIN: ')
    print(strasin)

    print('Scraping the product informations')
    aps = ProductDetailsScraper(asin=strasin)
    product = aps.get_product_info()

    print('Scraping the product reviews starting from the most recent')
    ars = ProductReviewsScraper(
        asin=strasin, sort="recent"
    )
    reviews = ars.get_reviews()
    product.reviews = reviews

    print('Do you want to add it to the database?')
    while reply := input("type yes or no") not in ['yes', 'no']:
        pass

    if reply == "yes":
        db.session.add(product)
        db.session.add_all(reviews)
        db.session.commit()


if __name__ == "__main__":
    product_scrape()
