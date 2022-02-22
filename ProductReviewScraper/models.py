from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List


@dataclass
class Review():
    id: int = field(init=False)
    amazonid: str
    user: str
    rating: int
    title: str
    date: date
    verified: bool
    foreign: bool
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
    imageurl: str
    price: float
    global_ratings: int
    reviews: List[Review] = field(default_factory=list)

    def reviews_number(self):
        return len(self.reviews)

    def find_review(self, user):
        filter_review = [r for r in self.reviews if r.user == user]
        return filter_review[0] if filter_review else None

    def __repr__(self):
        return f"Product: {self.asin}  - {self.title}"

    def __str__(self):
        return self.__repr__()
