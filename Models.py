import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(100), nullable=False)


class Book(Base):
    __tablename__ = 'book'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(200), nullable=False)
    id_publisher = sa.Column(sa.Integer, sa.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='books')


class Shop(Base):
    __tablename__ = 'shop'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(100), nullable=False)


class Stock(Base):
    __tablename__ = 'stock'

    id = sa.Column(sa.Integer, primary_key=True)
    id_book = sa.Column(sa.Integer, sa.ForeignKey('book.id'), nullable=False)
    id_shop = sa.Column(sa.Integer, sa.ForeignKey('shop.id'), nullable=False)
    count = sa.Column(sa.Integer, nullable=False)

    book = relationship(Book, backref='stocks')
    shop = relationship(Shop, backref='stocks')


class Sale(Base):
    __tablename__ = 'sale'

    id = sa.Column(sa.Integer, primary_key=True)
    price = sa.Column(sa.Numeric(12, 2), nullable=False)
    date_sale = sa.Column(sa.TIMESTAMP, nullable=False)
    id_stock = sa.Column(sa.Integer, sa.ForeignKey('stock.id'), nullable=False)
    count = sa.Column(sa.Integer, nullable=False)

    stock = relationship(Stock, backref='sales')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

