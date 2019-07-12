import os
import logging
import json

from warehouse.models import Site, SiteTypes

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns = boto3.client('sns')
topic = os.environ['TOPIC']
msg_type = 'UPDATE_SITE'

message_attributes = {
    'msg_type': {
        'DataType': 'String',
        'StringValue': msg_type
    }
}


def update(event, context):
    """ Sends a message to update the Site, only name, zip_code, and type_id are 
    allowed to be changed

    Arguments:
        event {[type]} -- [description]
        context {[type]} -- [description]
    """

    if (type(event) == str):
        event = event.replace("'", "\"")
        event = json.loads(event)

    if 'body' in event:
        event['body'] = event['body'].replace("'", "\"")
        body = json.loads(event['body'])

    if 'name' not in body:
        pass

    if 'zip_code' not in body:
        pass

    if 'type_id' not in body or body['type_id'] not in SiteTypes:
        pass

    site_id = event['pathParameters']['id']

    body['site_id'] = site_id

    try:
        response = {'statusCode': 200,
                    'body': json.dumps(body)}

        msg = sns.publish(TopicArn=topic,
                          Message=json.dumps(body),
                          MessageAttributes=message_attributes)

        logger.info(msg)
    except Exception as ex:
        logger.error(ex)

        response = {'statusCode': 500, 'body': json.dumps({
            'errorMsg': str(ex)
        })}

    return response
