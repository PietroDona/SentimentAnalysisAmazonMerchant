# http requests and HTML parsing
import requests
from bs4 import BeautifulSoup as bsoup
from bs4.element import Tag
# date parsing and typing
from typing import List
# custom review container
from AmazonReviewScraper.models import Product

from time import sleep
import logging

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

BASEURL_MERCHANT = "https://www.amazon.com/s?i=merchant-items"
DELAY = 0.8


class MerchantItemsScraper():
    '''Class that scrape the items sold by a merchant with me from the amazon website'''

    def __init__(self, me: str, verbose: bool = False, max_scrape=None) -> None:
        self.me = me
        self.max_scrape = max_scrape

        self.logger = logging.getLogger()

    def get_url(self, page) -> str:
        '''Formatting of the reviews URL'''
        return f"{BASEURL_MERCHANT}&me={self.me}&page={page}"

    def get_items(self) -> List[Product]:
        '''Scrape ALL the products sold by the merchant'''
        results = []
        page = 1
        # iterates on the pages until we get an empty page
        self.logger.info(f"Start scraping the products of {self.me}... ")
        while True:
            # chack page limit
            if self.max_scrape:
                if page > self.max_scrape:
                    break
            # scrape the page
            page_list = self.get_page(page)
            # check if empty
            if not page_list:
                break
            # append the page to the result
            results += page_list
            page += 1
        self.logger.info("Merchant scraping done.")
        return results

    def get_page(self, page) -> List[Product]:
        '''Scrape the review in a given page'''
        # We need a bit of delay not to be shadow banned from scraping amazon website.
        # If we go too fast the server will refuse our requests
        sleep(DELAY)
        # URL to scrape
        url_to_scrape = self.get_url(page)
        #
        self.logger.info(f"Start page {page} at the url {url_to_scrape} ")
        #
        r = requests.get(url_to_scrape, headers=HEADERS)
        soup = bsoup(r.text, 'html.parser')
        #
        self.logger.info(f"Connection status code: {r.status_code}")
        #
        div_items = soup.find_all(
            "div", {"data-component-type": "s-search-result"})
        result = [self.parse_item(item) for item in div_items]
        return result or None

    def parse_item(self, item: Tag) -> Product:
        '''Parse the review Tag in the dataclass cleaning the various properties'''
        asin = item.attrs.get("data-asin")
        product_name = item.find(
            "div", class_="s-title-instructions-style").get_text().strip()
        average_review_raw = item.find(
            "i", class_="a-icon").get_text().strip().split(" ")[0]

        self.logger.info(f"Scraped the product with asin {asin}. ")

        return Product(asin=asin, title=product_name,
                       average_review=float(average_review_raw))

    def get_clean_title(self, item: Tag) -> str:
        '''Clean the title from the HTML'''
        title = item.find(
            "a", {"data-hook": "review-title"}).get_text().strip()
        return title


if __name__ == "__main__":
    logging.basicConfig(filename='scrape_merchant.log', filemode='w',
                        format='%(asctime)s AMAZON-SCRAPER: %(message)s',
                        level=logging.INFO)
    ams = MerchantItemsScraper(me="A294P4X9EWVXLJ", max_scrape=2, verbose=True)
    print(ams.get_items())
