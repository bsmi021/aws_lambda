import json
import logging
import os
import time
import uuid
from datetime import datetime

import boto3
dynamodb = boto3.resource('dynamodb')

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s: %(message)s')

def create(event, context):
    #print(event)
    if type(event) == str:
        data = json.loads(event)
    else:
        data = json.loads(event['body'])
    

    if 'name' not in data:
        logging.error('Validation failed, name is required')
        raise Exception('Couldn\'t create the brand')

    timestamp = str(datetime.utcnow().timestamp())

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    brand = {
        'id': str(uuid.uuid4()),
        'name': data['name'],
        'createdAt': timestamp,
        'updatedAt': timestamp
    }
    
    # write to the database
    table.put_item(Item=brand)

    #create the response
    response = {
        'statusCode': 200,
        'body': json.dumps(brand)
    }

    return response