import json
import datetime

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from Models import create_tables, Publisher, Shop, Book, Stock, Sale

# print('Type username:')
# username = input()
# print('Type password:')
# password = int(input())
# print('Type SQL base name:')
# SQL_base_name = input()
# DNS = f'postgresql://{username}:{password}@localhost:5432/{SQL_base_name}'

DNS = 'postgresql://postgres:311089@localhost:5432/Netology_SQL'

engine = sa.create_engine(DNS)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as f:
    data = json.load(f)

model_dict = {
    'publisher': Publisher,
    'shop': Shop,
    'book': Book,
    'stock': Stock,
    'sale': Sale
}

for data_line in data:
    model = model_dict[data_line.get('model')]
    session.add(model(id=data_line.get('pk'), **data_line.get('fields')))
session.commit()

print('Write publisher id:')
publisher_id = int(input())

querry = sa.select(Book.title, Shop.name, Sale.price, Sale.date_sale).select_from(Book)\
    .join(Publisher, Publisher.id == Book.id_publisher)\
    .join(Stock, Stock.id_book == Book.id)\
    .join(Shop, Shop.id == Stock.id_shop)\
    .join(Sale, Sale.id == Stock.id).where(Publisher.id == publisher_id)

data_need = session.execute(querry).all()

for data_str in data_need:
    print(f'{data_str[0]:40} | {data_str[1]:5} | {float(data_str[2]):<5} | {data_str[3].strftime("%Y-%m-%d")}')
