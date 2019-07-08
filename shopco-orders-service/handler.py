import boto3
import json
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DECIMAL, Integer, DateTime
from sqlalchemy.orm import sessionmaker
import datetime as dt
from uuid import uuid4
import psycopg2
import os
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s: %(message)s')

# get environ vars
db_host = os.environ.get('host')
db_port = os.environ.get('port')
db_user = os.environ.get('user')
db_pass = os.environ.get('pass')
db_name = os.environ.get('db')
order_added_queue_name = os.environ.get('order_added_queue_name')

# postgress connection
db_uri = f'postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
Base = declarative_base()
db_engine = create_engine(db_uri)
logging.info(f'Connected to the {db_name} database.')
print('Connected')

# set connection to sqs
sqs = boto3.resource('sqs')
print(order_added_queue_name)
order_added_queue = sqs.get_queue_by_name(QueueName=order_added_queue_name)
logging.info(f"Connected to SQS - {order_added_queue_name}")

# class/table Order/order
class Order(Base):
    __schema__ = 'public'
    __tablename__ = 'order'

    id = Column(String, primary_key=True)
    order_date = Column(DateTime)
    order_amount = Column(DECIMAL)

    def __repr__(self):
        return "<Order(id='%s', order_date='%s', order_amt=%s>" % (self.id, self.order_date, self.order_amount)


def add_order_db(event, context):
    for record in event['Records']:
        print(record)
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


def add_order_sqs(event, context):
    """ Accepts order information, creates a new ID and Order Date, records in the database.

    Arguments:
        event {[object]} -- [description]
        context {[object]} -- [description]

    Returns:
        [string] -- The result
    """
    if (type(event) == str):
        event = event.replace("'", "\"")
        event = json.loads(event)

    if 'body' in event:
        event = json.loads(event['body'])

    # set the initial order properties in variables
    id = str(uuid4())
    order_date = dt.datetime.utcnow()
    order_amt = 0

    # if order_amout is missing from the payload set the value to 0, not looking for business rules atm
    if "orderAmount" in event:
        order_amt = event['orderAmount']
    else:
        order_amt = 0

    # create an instance of the order model
    order = Order(id=id, order_date=order_date, order_amount=order_amt)

    try:
        response = {'statusCode': 201,
                    'body': {'orderId': order.id, 'orderDate': str(order.order_date)}
                    }

        try:
            msg_body = {'orderId': order.id, 'orderDate': str(order.order_date), 'orderAmount': str(order.order_amount)}

            msg_body = json.dumps(msg_body)

            msg = order_added_queue.send_message(MessageBody=msg_body)

            if msg is not None:
                print(msg)
                logging.info(f'Sent SQS message ID: {msg["MessageId"]}')

        except ClientError as e:
            logging.error(e)

    except Exception as ex:
        print('Issue in submitting order -- %s' % order)
        logging.error('Issue in submitting order -- %s' % order)
        logging.error(ex)
        print(ex)

        response = {'statusCode': 500, 'body': {
            'errorMsg': str(ex)
        }}

    return json.dumps(response)
