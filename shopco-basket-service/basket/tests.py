import os
import json
import logging

if 'ENV' in os.environ:
    from models import Basket
else:
    from basket.models import Basket

if 'ENV' in os.environ:
    from create import create
else:
    from basket.create import create

if 'ENV' in os.environ:
    from delete import delete
else:
    from basket.delete import delete

if 'ENV' in os.environ:
    from update import update
else:
    from basket.update import update

if 'ENV' in os.environ:
    from list import list
else:
    from basket.list import list

if 'ENV' in os.environ:
    from get import get
else:
    from basket.get import get

logger = logging.getLogger()

if __name__ == "__main__":
    from uuid import uuid4
    import random
    # Tests the model against a local DynamoDB
    # docker run --rm -p 8000:8000 amazon/dynamodb-local:latest

    if not Basket.exists():
        Basket.create_table(read_capacity_units=100,
                            write_capacity_units=100, wait=True)

    customer_id = str(uuid4())

    print('###Test creating basket')
    for x in range(1, 6):
        item = {
            "customer_id": customer_id,
            "product_id": str(x),
            "price": random.uniform(0.99, 10.99),
            "quantity": random.randint(1, 10)
        }
        event = {
            'body': json.dumps(item)
        }
        print(json.dumps(create(event, None)))

    print()
    print('###Test getting basket')

    event = {'pathParameters': {
        'id': customer_id
    }}

    result = list(event, None)

    print(result)

    del_event = {
        'pathParameters': {
            'id': customer_id,
            'product_id': "2"
        }
    }

    print()
    print("###Test getting rid of an item")
    print(delete(del_event, None))

    print(list(event, None))

    print()

    print('###Test adding an existing item to pop the quantity')
    # get the item
    get_basket_event = {
        'pathParameters': {
            'id': customer_id,
            'product_id': '3'
        }
    }
    basket_item_3 = get(get_basket_event, None)

    print()
    print(basket_item_3)

    create_basket_3 = {
        'body': basket_item_3['body']
    }

    basket_item_3 = create(create_basket_3, None)

    print(basket_item_3)

    print('###Test update the quantity to be a specific value')

    basket_item_3 = json.loads(basket_item_3['body'])
    basket_item_3['quantity'] = -99

    update_basket_event = {
        'pathParameters': {'id': customer_id},
        'body': json.dumps({
            'product_id': basket_item_3['product_id'],
            'quantity': basket_item_3['quantity']
        })
    }

    print(update(update_basket_event, None))

