import json
import logging

from customers.models import CustomerModel

logger = logging.getLogger()


def update(event, context):
    data = json.loads(event['body'])

    id = event['pathParameters']['id']

    customer = CustomerModel.get(id)

    customer.first_name = data.get('first_name', customer.first_name)
    customer.last_name = data.get('last_name', customer.last_name)
    customer.email_addr = data.get('email_addr', customer.email_addr)
    customer.phone_number = data.get('phone_number', customer.phone_number)

    customer.save()

    return {
        'statusCode': 200,
        'body': json.dumps(dict(customer))
    }
