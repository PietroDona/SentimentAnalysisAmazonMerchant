'''
Interface to the sqlite database using sqlalchemy
'''

from ProductReview.models import Product, Review
from ProductReview.config import DBNAME
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, registry, relationship


metadata = MetaData()

product_table = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("asin", String(255)),
    Column("title", String(255)),
    Column("imageurl", String(255)),
    Column("price", Float),
    Column("global_ratings", Integer),
)
review_table = Table(
    "reviews",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("amazonid", String(255)),
    Column("user", String(255)),
    Column("rating", Integer),
    Column("title", String(255)),
    Column("date", Date),
    Column("verified", Boolean),
    Column("foreign", Boolean),
    Column("content", String(255)),
    Column("helpfulvote", Integer, default=0),
    Column("product_id", Integer, ForeignKey("products.id")),
)


# connection
engine = create_engine(f"sqlite:///{DBNAME}")

# create metadata
metadata.create_all(engine)

mapper_registry = registry()

mapper_registry.map_imperatively(
    Product,
    product_table,
    properties={
        "reviews": relationship(Review, backref="product", order_by=review_table.c.id),
    },
)
mapper_registry.map_imperatively(Review, review_table, properties={})

# create session
Session = sessionmaker(bind=engine)
session = Session()
