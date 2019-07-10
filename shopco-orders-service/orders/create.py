import os
import logging
import json
from uuid import uuid4
import datetime as dt

import boto3
from botocore.exceptions import ClientError
from orders.models import Order

logger = logging.getLogger()

#logger.basicConfig(level=logging.DEBUG,
 #                   format='%(levelname)s: %(asctime)s: %(message)s')

#logger = logging.get_logger()

# create the sns client
sns = boto3.client('sns')
topic = os.environ['TOPIC']



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
    #order = Order(order_id=id, order_date=order_date, order_amount=order_amt)

    event['order_id'] = id
    event['order_date'] = str(order_date)

    try:
        response = {'statusCode': 201,
                    'body': json.dumps(event)
                    }

        try:
            #msg_body = {'orderId': order.id, 'orderDate': str(order.order_date), 'orderAmount': str(order.order_amount)}

            msg_body = json.dumps(event)

            msg = sns.publish(TopicArn=topic, Message=msg_body)

            print(msg)
            logger.info(msg)

        except ClientError as e:
            logger.error(e)

    except Exception as ex:
        print('Issue in submitting order -- %s' % order)
        logger.error('Issue in submitting order -- %s' % order)
        logger.error(ex)
        print(ex)

        response = {'statusCode': 500, 'body': json.dumps( {
            'errorMsg': str(ex)
        })}

    return response