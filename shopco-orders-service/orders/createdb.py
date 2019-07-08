import os
import logging
import json

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DECIMAL, Integer, DateTime
from sqlalchemy.orm import sessionmaker

from orders.models import Order

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s: %(message)s')

db_host = os.environ.get('host')
db_port = os.environ.get('port')
db_user = os.environ.get('user')
db_pass = os.environ.get('pass')
db_name = os.environ.get('db')

db_uri = f'postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
#Base = declarative_base()
db_engine = create_engine(db_uri)
logging.info(f'Connected to the {db_name} database.')
print('Connected')

def insert(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])
        order_id = body['orderId']
        order_date = body['orderDate']
        order_amount = body['orderAmount']

        order = Order(id=order_id, order_date=order_date, order_amount=order_amount)

        try:
            # create a session
            Session = sessionmaker(bind=db_engine)
            session = Session()

            # add the order to the session
            session.add(order)
            session.commit()

        except Exception as ex:
            logging.error('Issue in submitting order -- %s' % order)
            logging.error(ex)