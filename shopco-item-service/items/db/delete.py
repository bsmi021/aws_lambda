import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def delete(event, context):
    
    if type(event) == str:
        event = json.loads(event)

    for record in event['Records']:
        data = json.loads(record['Sns']['Message'])

        table.delete_item(
            Key={
                'id': data['id']
            }
        )

    response = {
        'statusCode': 200
    }

    return response