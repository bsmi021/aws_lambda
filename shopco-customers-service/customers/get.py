import json

from pynamodb.exceptions import DoesNotExist
from customers.models import CustomerModel

def get(event, context):
    try:
        customer = CustomerModel.get(hash_key=event['pathParameters']['id'])
    except DoesNotExist:
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'Customer was not found'})}
    
    return {'statusCode': 200,
            'body': json.dumps(dict(customer))}