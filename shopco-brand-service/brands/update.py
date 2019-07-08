import json
import time
import logging
import os

from brands import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')

def update(event, context):
    print(event)

    data = json.loads(event['body'])
    if 'name' not in data:
        logging.error('Validation failed')
        raise Exception('Could not update brand')
        return
    
    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # check if the brand exists
    brand = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    if 'Item' not in brand:
        response = {
            'statusCode': 500,
            'body': json.dumps({'msg': 'Invald brand'})
        }
    else:
        result = table.update_item(
            Key={
                'id': event['pathParameters']['id']
            },
            ExpressionAttributeNames={
                '#brand_name': 'name',
            },
            ExpressionAttributeValues={
                ':name': data['name'],
                ':updatedAt': timestamp,
            },
            UpdateExpression='SET #brand_name = :name, updatedAt = :updatedAt',
            ReturnValues='ALL_NEW'
        )

        # create the response
        response = {
            'statusCode': 200,
            'body': json.dumps(result['Attributes'],
                               cls=decimalencoder.DecimalEncoder)
        }

    return response