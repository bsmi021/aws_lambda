import os
import logging
import json
from uuid import uuid4
import datetime as dt

from warehouse.models import Site, SiteTypes

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns = boto3.client('sns')
topic = os.environ['TOPIC']

def create(event, context):
    """ Sends an event creationg request to the SNS Topic
    
    Arguments:
        event {[type]} -- [description]
        context {[type]} -- [description]
    """
    if (type(event) == str):
        event = event.replace("'", "\"")
        event = json.loads(event)

    if 'body' in event:
        event['body'] = event['body'].replace("'", "\"")
        event = json.loads(event['body'])

    if 'name' not in event:
        pass
    
    if 'zip_code' not in event:
        pass

    if 'type_id' not in event or event['type_id'] not in SiteTypes:
        pass

    id = str(uuid4())

    event['site_id'] = id

    try:
        response = {'statusCode': 200,
                    'body': json.dumps(event)
            }
        
        msg = sns.publish(TopicArn=topic, Message=json.dumps(event))

        logger.info(msg)
    except Exception as ex:
        logger.error(ex)
        response = {'statusCode': 500, 'body': json.dumps( {
            'errorMsg': str(ex)
        })}

    return response