import os
import json
import logging

if 'ENV' in os.environ:
    from models import Basket
else:
    from basket.models import Basket

logger = logging.getLogger()


def list(event, context):
    customer_id = event['pathParameters']['id']

    basket = Basket.query(customer_id)

    return {
        'statusCode': 200,
        'body': json.dumps(
            {'items':
                [dict(result) for result in basket]
             }
        )
    }
