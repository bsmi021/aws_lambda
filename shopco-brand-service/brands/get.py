import os
import json

from brands import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # get the brand from the db
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    if 'Item' in result:
        # create the response
        response = {
            'statusCode': 200,
            'body': json.dumps(result['Item'],
                               cls=decimalencoder.DecimalEncoder)
        }
    else:
        response = {
            'statusCode': 500,
            'body': json.dumps({'msg': 'Brand Not Found'},
                               cls=decimalencoder.DecimalEncoder)
        }
    return response
