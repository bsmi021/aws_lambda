import os
import json
import logging

if 'ENV' in os.environ:
    from models import Basket
else:
    from basket.models import Basket

logger = logging.getLogger()


def get(event, context):
    customer_id = event['pathParameters']['id']
    item_id = event['pathParameters']['product_id']

    try:
        basket = Basket.get(customer_id, item_id)

        return {
            'statusCode': 200,
            'body': basket.body()
        }
    except:
        raise Exception("Invalid request")

