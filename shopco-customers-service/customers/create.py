import json
import logging
import uuid

from customers.models import CustomerModel


def create(event, context):
    data = json.loads(event['body'])
    if 'last_name' not in data:
        logging.error('Validation failed')
        return {
            'statusCode': 422,
            'body': json.dumps({'error_message': 'Could\'t create the customer item.'})
        }

    if not data['first_name'] or not data['last_name']:
        logging.error(
            'Validation failed - first name or last name was empty. %s', data)
        return {
            'statusCode': 422,
            'body': json.dumps({'error_message': 'Couldn\'t create the customer, name values missing'})
        }

    customer = CustomerModel(id=str(uuid.uuid4()),
                             first_name=data['first_name'],
                             last_name=data['last_name'],
                             email_addr=data['email_addr'])

    customer.save()

    return {'statusCode': 200,
            'body': json.dumps(dict(customer))}
