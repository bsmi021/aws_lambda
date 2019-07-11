import os
import logging
import json
from datetime import datetime


from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DECIMAL, Integer, DateTime
from sqlalchemy.orm import sessionmaker

from orders.models import Order, Address, Buyer, OrderItem, PaymentMethod


logger = logging.getLogger()

db_host = os.environ.get('host')
db_port = os.environ.get('port')
db_user = os.environ.get('user')
db_pass = os.environ.get('pass')
db_name = os.environ.get('db')

db_uri = f'postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
#Base = declarative_base()
db_engine = create_engine(db_uri)
logger.info(f'Connected to the {db_name} database.')
logger.info('Connected')

def insert(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])
        body = json.loads(body['Message'])
        order_id = body['order_id']
        order_date = body['order_date']
        #order_amount = body['order_amount']

        address = body['address']

        if type(address) is str:
            address = json.loads(address)

        address = Address(address['street_1'], address['street_2'], address['city'], address['state'], address['country'], address['zip_code'])

        order = Order(order_id=order_id, order_date=order_date, customer_id=body['customer_id'], address=address)

        order.created_at = datetime.utcnow()
        order.updated_at = datetime.utcnow()

        try:
            # create a session
            Session = sessionmaker(bind=db_engine)
            session = Session()

            # add the order to the session
            session.add(order)
            session.commit()

            logger.info(order)

        except Exception as ex:
            logger.error('Issue in submitting order -- %s' % order)
            logger.error(ex)