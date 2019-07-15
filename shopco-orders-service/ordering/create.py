import json
import logging
from uuid import uuid4
from ordering.models import *

logger = logging.getLogger()


def create(event, context):
    data = json.loads(event['body'])

    order = Order()

    order.customer_id = data['customer_id']

    ship_address = OrderAddress(street_1=data['ship_address']['street_1'],
                                street_2=data['ship_address']['street_2'],
                                city=data['ship_address']['city'],
                                state=data['ship_address']['state'],
                                zip_code=data['ship_address']['zip_code'],
                                country=data['ship_address']['country']
                                )

    bill_address = OrderAddress(street_1=data['bill_address']['street_1'],
                                street_2=data['bill_address']['street_2'],
                                city=data['bill_address']['city'],
                                state=data['bill_address']['state'],
                                zip_code=data['bill_address']['zip_code'],
                                country=data['bill_address']['country']
                                )

    buyer = Buyer(first_name=data['buyer']['first_name'],
                  last_name=data['buyer']['last_name'],
                  email_address=data['buyer']['email_address'],
                  phone_number=data['buyer']['phone_number'])

    order.buyer = buyer
    order.ship_addr = ship_address
    order.bill_addr = bill_address
    order.pay_method = PaymentMethod(card_number=data['cc_num'],
                                     expiration=data['cc_expr'],
                                     ccv=data['ccv'],
                                     card_type=data['card_type'])

    order.status = 'POSTED'

    order.line_items = []
    order_total = 0

    for item in data['line_items']:
        order_item = OrderItem(product_id=item['product_id'],
                               product_name=item['product_name'],
                               unit_price=item['unit_price'],
                               quantity=item['quantity'])
        order_item.set_line_total()
        order.line_items.append(order_item)

        order_total += order_item.line_total

    order.order_total = order_total

    order.save()

    return {'statusCode': 200,
            'body': json.dumps(dict(order))}
