from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Review():
    user: str
    rating: int
    title: str
    date: date
    verified: bool
    content: str
    helpfulvote: Optional[int]

    def dict(self):
        return {"user": self.user,
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
    title: str
    average_review: float

    def __repr__(self):
        return f"Product: {self.asin}  - {self.title}"

    def __str__(self):
        return self.__repr__()


@dataclass
class Merchant():
    name: str
    me: str

    def __repr__(self):
        return f"Merchant: {self.name}  - {self.me}"

    def __str__(self):
        return self.__repr__()
