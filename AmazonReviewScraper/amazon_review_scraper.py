# http requests and HTML parsing
import requests
from bs4 import BeautifulSoup as bsoup
from bs4.element import Tag
# date parsing and typing
from dateutil.parser import parse as date_parser
from datetime import date
from typing import List
from time import sleep
# custom review container
from models import Review
import logging

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
BASEURL_REVIEW = "https://www.amazon.com/product-reviews"
DELAY = 0.8


class ProductReviewScraper():
    '''Class that scrape the reviews of the product with given asin from the amazon website'''

    def __init__(self, asin: str, sort: str = 'recent', verbose: bool = False, max_scrape=None) -> None:
        # Order the reviews
        sort_types = ['recent', 'helpful']
        if sort not in sort_types:
            raise ValueError(
                f"Invalid sort type. Expected one of: {sort_types}")
        # if verbose:

        self.logger = logging.getLogger()

        self.asin = asin
        self.sort = sort
        self.max_scrape = max_scrape

    def get_url(self, page) -> str:
        '''Formatting of the reviews URL'''
        return f"{BASEURL_REVIEW}/{self.asin}/ref=cm_cr_arp_d_viewopt_srt?sortBy={self.sort}&pageNumber={page}"

    def get_reviews(self) -> List[Review]:
        '''Scrape ALL the reviews of the product'''
        results = []
        page = 1
        self.logger.info(f"Start scraping the reviews of {self.asin}... ")
        # iterates on the pages until we get an empty page
        while True:
            # chack page limit
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
        self.logger.info("Reviews scraping done.")
        return results

    def get_page(self, page) -> List[Review]:
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
        div_reviews = soup.find_all(
            "div", id=lambda x: x and x.startswith('customer_review-'))
        result = [self.parse_review(item) for item in div_reviews]
        return result or None

    def parse_review(self, item: Tag) -> Review:
        '''Parse the review Tag in the dataclass cleaning the various properties'''

        user = self.get_clean_user(item)
        rating = self.get_clean_rating(item)
        title = self.get_clean_title(item)
        date = self.get_clean_date(item)
        verified = self.get_clean_verified(item)
        content = self.get_clean_content(item)
        helpfulvote = self.get_clean_helpfulvote(item)
        self.logger.info(f"Scraped the review by user {user}. ")

        return Review(**{"user": user,
                         "rating": rating,
                         "title": title,
                         "date": date,
                         "verified": verified,
                         "content": content,
                         "helpfulvote": helpfulvote})

    def get_clean_user(self, item: Tag) -> str:
        '''Clean the user id from the HTML'''
        user = item.find("a", class_="a-profile")
        user_link = user.get('href')
        user_id = user_link.split("/")[3].split(".")[-1]
        return user_id

    def get_clean_rating(self, item: Tag) -> int:
        '''Clean the rating from the HTML'''
        rating = item.find("span", class_="a-icon-alt").get_text().strip()
        rating_int = int(rating[0])
        return rating_int

    def get_clean_title(self, item: Tag) -> str:
        '''Clean the title from the HTML'''
        title = item.find(
            "a", {"data-hook": "review-title"}).get_text().strip()
        return title

    def get_clean_date(self, item: Tag) -> date:
        '''Clean the date from the HTML'''
        # from here I can extract also the country - not implemented
        meta = item.find(
            "span", {"data-hook": "review-date"}).get_text()
        raw_date = meta.split("on")[-1].strip()
        return date_parser(raw_date).date()

    def get_clean_verified(self, item: Tag) -> bool:
        '''Clean the verified buy from the HTML'''
        return item.find("span", {"data-hook": "avp-badge"}) is not None

    def get_clean_content(self, item: Tag) -> date:
        '''Clean the content of the review from the HTML'''
        # from here I can extract also the country - not implemented
        content = item.find(
            "span", {"data-hook": "review-body"}).get_text().strip()
        return content

    def get_clean_helpfulvote(self, item: Tag) -> int or None:
        '''Clean the number of helpful votes from the HTML'''
        helpfulvote = item.find(
            "span", {"data-hook": "helpful-vote-statement"})
        if not helpfulvote:
            return None
        helpfulvote_text = helpfulvote.get_text().lower()
        helpfulvote_number = helpfulvote_text.split(
            " ")[0].replace("one", "1").replace(",", "").replace(".", "")
        return(int(helpfulvote_number))


if __name__ == "__main__":
    logging.basicConfig(filename='scrape_review.log', filemode='w',
                        format='%(asctime)s AMAZON-SCRAPER: %(message)s', level=logging.INFO)
    ars = ProductReviewScraper(asin="B07L32B9C2", sort="helpful",
                               max_scrape=2, verbose=True)
    print(ars.get_reviews())
