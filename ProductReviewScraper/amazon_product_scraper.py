'''
Web scraper of the Amazon product details
ProductDetailsScraper - Class containig the scraper
'''
# http requests and HTML parsing
import requests
from bs4 import BeautifulSoup as bsoup

# custom review container
from ProductReviewScraper.models import Product
from ProductReviewScraper.config import HEADERS, BASEURL_PRODUCT

import logging


class ProductDetailsScraper:
    '''Class that scrape the reviews of the product with given asin from the amazon website'''

    def __init__(
        self,
        asin: str
    ) -> None:
        self.logger = logging.getLogger()
        self.asin = asin
        self.product = None

    def get_url(self) -> str:
        '''Formatting of the reviews URL'''
        return f"{BASEURL_PRODUCT}/{self.asin}"

    def _get_product_info(self) -> None:
        '''Scrape the product info from the Amazon Website'''
        # URL to scrape
        url_to_scrape = self.get_url()
        #
        self.logger.info(
            f"Start scarping the basic product info at the url {url_to_scrape}")
        #
        r = requests.get(url_to_scrape, headers=HEADERS)
        soup = bsoup(r.text, "html.parser")
        #
        self.logger.info(f"Connection status code: {r.status_code}")
        #

        scraped_title = soup.find(
            "span", id="productTitle").get_text().strip()
        scraped_price = float(soup.find(
            "span", {"class": "a-price"}).find(
                "span", {"class": "a-offscreen"}).get_text().strip()[1:].replace(",", ""))
        scraped_imageurl = soup.find(
            "img", id="landingImage").get("src")

        scraped_global_ratings = int(soup.find(
            "span", id="acrCustomerReviewText").get_text().strip()[:-7].strip().replace(",", ""))
        self.product = Product(asin=self.asin, title=scraped_title,
                               price=scraped_price, imageurl=scraped_imageurl,
                               global_ratings=scraped_global_ratings)
        self.logger.info(f"Product {self.asin} scaped successfully")

    def get_product_info(self) -> Product:
        if not self.product:
            self._get_product_info()
        return self.product
