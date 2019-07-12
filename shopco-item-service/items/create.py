import boto3
import json
import datetime as dt
from uuid import uuid4
import os

# create the sns client
sns = boto3.client('sns')
topic = os.environ['TOPIC']


def errorResponse(attributeName):
    return {
        'statusCode': 422,
        'body': json.dumps({
            "error": f"Required attribute {attributeName} is missing."
        })
    }


def create(event, context):

    if type(event) is str:
        data = json.loads(event)

    data = json.loads(event['body'])

    timestamp = str(dt.datetime.utcnow())

    if 'sku' not in data:
        return errorResponse('sku')

    if 'name' not in data:
        return errorResponse('name')

    if 'price' not in data:
        return errorResponse('price')

    if 'description' not in data:
        data['description'] = ''

    if 'attributes' not in data:
        data['attributes'] = '[]'

    if 'product_brand' not in data:
        return errorResponse('product_brand')

    data['id'] = str(uuid4())
    data['createdAt'] = timestamp
    data['updatedAt'] = timestamp
    data['is_deleted'] = False

    response = sns.publish(TopicArn=topic,
                           Message=json.dumps(data))

    return {
        'statusCode': 200,
        'body': json.dumps({'id': data['id']})
    }
