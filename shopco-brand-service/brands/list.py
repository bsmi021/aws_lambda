import os
import json

from brands import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')

def list(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch all the rows in the table
    result = table.scan()

    # create the response
    if 'Items' in result:
        response = {
            'statusCode': 200,
            'body': json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)

        }
    else:
        response = {
            'statusCode': 200,
            'body': []
        }

    return response