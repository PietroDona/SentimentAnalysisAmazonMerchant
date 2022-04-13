'''
Web scraper of the Amazon product reviews
ProductReviewsScraper - Class containig the review scraper
'''
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
from ProductReviewScraper.models import Review
from ProductReviewScraper.config import HEADERS, BASEURL_REVIEW, DELAY

import logging


class ProductReviewsScraper:
    """Class that scrape the reviews of the product with given asin from the amazon website"""

    def __init__(
        self,
        asin: str,
        sort: str = "recent",
        max_scrape: int = None,
    ) -> None:
        # Order the reviews
        sort_types = ["recent", "helpful"]
        if sort not in sort_types:
            raise ValueError(
                f"Invalid sort type. Expected one of: {sort_types}")
        # if verbose:

        self.logger = logging.getLogger()

        self.asin = asin
        self.sort = sort
        self.max_scrape = max_scrape

    def get_url(self, page) -> str:
        """Formatting of the reviews URL"""
        return f"{BASEURL_REVIEW}/{self.asin}/ref=cm_cr_arp_d_viewopt_srt?sortBy={self.sort}&pageNumber={page}"

    def get_reviews(self) -> List[Review]:
        """Scrape ALL the reviews of the product"""
        results = []
        page = 1
        self.logger.info(f"Start scraping the reviews of {self.asin}... ")
        # iterates on the pages until we get an empty page
        while True:
            # # check page limit
            if self.max_scrape:
                if page > self.max_scrape:
                    break
            # scrape the page
            page_list = self.get_page(page)
            self.logger.info(page_list)
            # check if empty
            if not page_list:
                break
            # append the page to the result
            results += page_list
            page += 1
            # We need a bit of delay not to be shadow banned from scraping amazon website.
            # If we go too fast the server will refuse our requests
            sleep(DELAY)
        self.logger.info("Reviews scraping done.")
        return results

    def get_page(self, page) -> List[Review]:
        """Scrape the review in a given page"""
        # URL to scrape
        url_to_scrape = self.get_url(page)
        #
        self.logger.info(f"Start page {page} at the url {url_to_scrape} ")
        #
        r = requests.get(url_to_scrape, headers=HEADERS)
        soup = bsoup(r.text, "html.parser")
        #
        self.logger.info(f"Connection status code: {r.status_code}")
        #
        div_reviews = soup.find_all("div", {"data-hook": "review"})
        result = [self.parse_review(item) for item in div_reviews]
        return result or None

    def parse_review(self, item: Tag) -> Review:
        """Parse the review Tag in the dataclass cleaning the various properties"""
        amazonid = item.get("id")
        user = self.get_clean_user(item)
        rating = self.get_clean_rating(item)
        title = self.get_clean_title(item)
        date = self.get_clean_date(item)
        verified = self.get_clean_verified(item)
        foreign, content = self.get_clean_content(item)
        helpfulvote = self.get_clean_helpfulvote(item)
        self.logger.info(f"Scraped the review by user {user}. ")

        return Review(
            amazonid=amazonid,
            user=user,
            rating=rating,
            title=title,
            date=date,
            verified=verified,
            content=content,
            foreign=foreign,
            helpfulvote=helpfulvote,
        )

    def get_clean_user(self, item: Tag) -> str:
        """Clean the user id from the HTML"""
        user = item.find("span", class_="a-profile-name").get_text().strip()
        return user

    def get_clean_rating(self, item: Tag) -> int:
        """Clean the rating from the HTML"""
        rating = item.find("span", class_="a-icon-alt").get_text().strip()
        rating_int = int(rating[0])
        return rating_int

    def get_clean_title(self, item: Tag) -> str:
        """Clean the title from the HTML"""
        title = item.find(attrs={"data-hook": "review-title"})
        # check_if_translated
        translated_title = title.find(
            "span", class_="cr-original-review-content")
        if translated_title:
            return translated_title.get_text().strip()
        return title.get_text().strip()

    def get_clean_date(self, item: Tag) -> date:
        """Clean the date from the HTML"""
        # from here I can extract also the country - not implemented
        meta = item.find("span", {"data-hook": "review-date"}).get_text()
        raw_date = meta.split("on")[-1].strip()
        return date_parser(raw_date).date()

    def get_clean_verified(self, item: Tag) -> bool:
        """Clean the verified buy from the HTML"""
        return item.find("span", {"data-hook": "avp-badge"}) is not None

    def get_clean_content(self, item: Tag) -> date:
        """Clean the content of the review from the HTML"""
        # from here I can extract also the country - not implemented
        content = item.find(
            "span", {"data-hook": "review-body"})

        if not content:
            return False, ""
        # check_if_translated
        translated_content = content.find(
            "span", class_="cr-original-review-content")
        if translated_content:
            return True, translated_content.get_text().strip()

        if not content.find("span"):
            return False, ""

        return False, content.find("span").get_text().strip()

    def get_clean_helpfulvote(self, item: Tag) -> int or None:
        """Clean the number of helpful votes from the HTML"""
        helpfulvote = item.find(
            "span", {"data-hook": "helpful-vote-statement"})
        if not helpfulvote:
            return None
        helpfulvote_text = helpfulvote.get_text().lower()
        helpfulvote_number = (
            helpfulvote_text.split(" ")[0]
            .replace("one", "1")
            .replace(",", "")
            .replace(".", "")
        )
        return int(helpfulvote_number)
