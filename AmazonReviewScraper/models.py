from dataclasses import dataclass, asdict
from datetime import date
from typing import Optional


@dataclass
class Review():
    user: str
    asin: str
    rating: int
    title: str
    date: date
    verified: bool
    content: str
    helpfulvote: Optional[int]

    def dict(self):
        return {"user": self.user,
                "asin": self.asin,
                "rating": self.rating,
                "title": self.title,
                "date": self.date.isoformat(),
                "verified": self.verified,
                "content": self.content,
                "helpfulvote": self.helpfulvote
                }

    def __repr__(self):
        return f"Review by {self.user} with title {self.title}"

    def __str__(self):
        return self.__repr__()


@dataclass
class Product():
    asin: str
    product: str
    average_review: float
    # merchant name
    producer: Optional[str]
    # merchant token
    me: Optional[str]

    def __repr__(self):
        return f"Product: {self.asin}  - {self.product} by {self.producer or self.me}"

    def __str__(self):
        return self.__repr__()
