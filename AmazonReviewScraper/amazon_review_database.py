from AmazonReviewScraper.models import Merchant, Product, Review

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, registry, relationship


metadata = MetaData()
merchant_table = Table('merchants', metadata,
                       Column('id', Integer, primary_key=True,
                              autoincrement=True),
                       Column('me', String(255)),
                       Column('name', String(255))
                       )
product_table = Table('products', metadata,
                      Column('id', Integer, primary_key=True,
                             autoincrement=True),
                      Column('asin', String(255)),
                      Column('title', String(255)),
                      Column('average_review', Float),
                      Column('merchant_id', Integer,
                             ForeignKey('merchants.id'))
                      )
review_table = Table('reviews', metadata,
                     Column('id', Integer, primary_key=True,
                            autoincrement=True),
                     Column('user', String(255)),
                     Column('rating', Integer),
                     Column('title', String(255)),
                     Column('date', Date),
                     Column('verified', Boolean),
                     Column('content', String(255)),
                     Column('helpfulvote', Integer, nullable=True),
                     Column('product_id', Integer,
                            ForeignKey('products.id'))
                     )


# connection
engine = create_engine('sqlite:///reviews.db')

# create metadata
metadata.create_all(engine)

mapper_registry = registry()
mapper_registry.map_imperatively(Merchant, merchant_table, properties={
    'products': relationship(Product, backref='merchant', order_by=product_table.c.id),
})
mapper_registry.map_imperatively(Product, product_table, properties={
    'reviews': relationship(Review, backref='product', order_by=review_table.c.id),
})
mapper_registry.map_imperatively(Review, review_table, properties={})

# create session
Session = sessionmaker(bind=engine)
session = Session()
