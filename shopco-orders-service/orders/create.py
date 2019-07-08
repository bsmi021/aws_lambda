import os
import logging
import json
from uuid import uuid4
import datetime as dt

import boto3
from botocore.exceptions import ClientError
from orders.models import Order

queue_name = os.environ.get('QUEUE_NAME')

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s: %(message)s')

# set connection to sqs
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName=queue_name)

logging.info(f"Connected to SQS - {queue_name}")


def create(event, context):
    if (type(event) == str):
        event = event.replace("'", "\"")
        event = json.loads(event)

    if 'body' in event:
        event['body'] = event['body'].replace("'", "\"")
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
                    'body': json.dumps({'orderId': order.id, 'orderDate': str(order.order_date)})
                    }

        try:
            msg_body = {'orderId': order.id, 'orderDate': str(order.order_date), 'orderAmount': str(order.order_amount)}

            msg_body = json.dumps(msg_body)

            msg = queue.send_message(MessageBody=msg_body)

            if msg is not None:
                print(msg['messageId'])
                logging.info(f'Sent SQS message ID: {msg["messageId"]}')

        except ClientError as e:
            logging.error(e)

    except Exception as ex:
        print('Issue in submitting order -- %s' % order)
        logging.error('Issue in submitting order -- %s' % order)
        logging.error(ex)
        print(ex)

        response = {'statusCode': 500, 'body': json.dumps( {
            'errorMsg': str(ex)
        })}

    return response