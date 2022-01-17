from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List


@dataclass
class Review():
    id: int = field(init=False)
    user: str
    rating: int
    title: str
    date: date
    verified: bool
    content: str
    helpfulvote: Optional[int]
    product_id: int = field(init=False)

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
    id: int = field(init=False)
    asin: str
    title: str
    average_review: float
    merchant_id: int = field(init=False)
    reviews: List[Review] = field(default_factory=list)

    def reviews_number(self):
        return len(self.reviews)

    def __repr__(self):
        return f"Product: {self.asin}  - {self.title}"

    def __str__(self):
        return self.__repr__()


@dataclass
class Merchant():
    id: int = field(init=False)
    name: str
    me: str
    products: List[Product] = field(default_factory=list)

    def __repr__(self):
        return f"Merchant: {self.name}  - {self.me}"

    def __str__(self):
        return self.__repr__()
