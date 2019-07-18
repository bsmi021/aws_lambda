import os
import json
import logging

if 'ENV' in os.environ:
    from models import Basket
else:
    from basket.models import Basket

logger = logging.getLogger()


def delete(event, context):
    """Removes an item from the customer basket

    Arguments:
        event {object} -- Event payload
        context {object} -- Lambda context
    """

    try:
        basket_item = Basket.get(event['pathParameters']['id'],
                                 event['pathParameters']['product_id'])

        basket_item.delete()

        return {
            'statusCode': 200
        }
    except Exception as ex:
        logger.error(ex)
        raise Exception("Invalid request")
