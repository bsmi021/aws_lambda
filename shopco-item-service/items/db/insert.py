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

table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def insert(event, context):
    
    if type(event) == str:
        event = json.loads(event)
    
    for record in event['Records']:
        data = json.loads(record['Sns']['Message'])

        table.put_item(Item=data)

        
    

    