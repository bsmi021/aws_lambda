import os
import json
import logging

if 'ENV' in os.environ:
    from models import Basket
else:
    from basket.models import Basket

logger = logging.getLogger()


def update(event, context):
    #    if 'requestContext' in event:
    #        if 'identity' in event['requestContext']:
    #            if 'cognitoIdentityId' in event['requestContext']['identity']:
    #                id = event['requestContext']['identity']['cognitoIdentityId']
    #    else:
    id = event['pathParameters']['id']

    data = json.loads(event['body'])

    product_id = data['product_id']

    try:
        basket = Basket.get(id, product_id)

        basket.quantity = data['quantity']

        basket.save()

        return {
            'statusCode': 200,
            'body': {
                basket.body()
            }
        }
    except Exception as ex:
        logger.error(ex)
        raise Exception("Invalid request")
