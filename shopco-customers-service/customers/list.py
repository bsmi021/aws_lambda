import json

from customers.models import CustomerModel


def list(event, context):
    results = CustomerModel.scan()

    return {
        'statusCode': 200,
        'body': json.dumps({
            'customers': [dict(result) for result in results]
        })
    }
