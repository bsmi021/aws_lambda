import os
import json
import logging

if 'ENV' in os.environ:
    from models import Basket
else:
    from basket.models import Basket

logger = logging.getLogger()


def create(event, context):
    data = json.loads(event['body'])

    customer_id = data['customer_id']
    product_id = data['product_id']
    basket = None

    # check if the item is in the basket already, if so we're gonna just add to it
    try:
        basket = Basket.get(customer_id, product_id)

        if basket is not None:
            basket.quantity = basket.quantity + data['quantity']
    except:
        pass

    if basket is None:
        basket = Basket(customer_id=customer_id,
                        product_id=product_id,
                        quantity=data['quantity'],
                        price=data['price'])

    basket.save()

    return {
        "statusCode": 200,
        "body": basket.body()
    }



