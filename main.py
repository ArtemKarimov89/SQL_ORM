import json
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from Models import create_tables, Publisher, Shop, Book, Stock, Sale


def create_session():
    print('Type username:')
    username = input()
    print('Type password:')
    password = int(input())
    print('Type SQL base name:')
    SQL_base_name = input()
    DNS = f'postgresql://{username}:{password}@localhost:5432/{SQL_base_name}'
    engine = sa.create_engine(dns)
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    new_session = Session()
    return new_session


def write_data_into_bd(session):
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


def get_shop(input_data):
    query = sa.select(Book.title, Shop.name, Sale.price, Sale.date_sale).select_from(Book) \
        .join(Publisher, Publisher.id == Book.id_publisher) \
        .join(Stock, Stock.id_book == Book.id) \
        .join(Shop, Shop.id == Stock.id_shop) \
        .join(Sale, Sale.id == Stock.id)
    if input_data.isdigit():
        query = query.where(Publisher.id == input_data)
    else:
        query = query.where(Publisher.name == input_data)
    data_need = session.execute(query).all()

    for book_name, shop_name, sale_price, sale_data in data_need:
        print(f'{book_name:<40} | {shop_name:<5} | {sale_price:<5} | {sale_data.strftime("%Y-%m-%d")}')


if __name__ == '__main__':
    session = create_session()
    write_data_into_bd(session)
    input_data = input('Write publisher id or name: ')
    get_shop(input_data)
