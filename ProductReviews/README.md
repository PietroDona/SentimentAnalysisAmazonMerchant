# Collect Amazon.com Product Reviews

Python package to download product review data from amazon.com based on the [ASIN code](https://en.wikipedia.org/wiki/Amazon_Standard_Identification_Number) (Amazon Standard Identification Number) of the product.

The script is based on `request` and `BeautifulSoup4`.

The data is parsed looking for `data-hook` attributes in the page and is stored in dataclasses.

-   `amazon_product_scraper` contains the class that collects the basic information about the product. At the moment, it collects

    -   asin
    -   title (of the insertion)
    -   imageurl (the url of the image of the product)
    -   price (current price, if the product is out of stock, the class could crash. An exception handler should be implemented.)
    -   global ratings (the global rating of the product)

-   `amazon_review_scraper` contains the class that collects the basic information about a single review. At the moment, it collects

    -   amazonid (we keep track of the review ID)
    -   user (the username of the reviewer)
    -   rating (the rating given in the review)
    -   title
    -   content
    -   date
    -   verified (if the reviewer purchased the product)
    -   foreign (if the review is written in English)
    -   helpful votes (how many times, if any, the review has been deemed useful by other users)

-   `amazon_review_database` contains the methods to store the collected data into a sqlite database using `sqlalchemy` ORM.
