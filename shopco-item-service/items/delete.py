import os
import json

import boto3

sns = boto3.client('sns')
topic = os.environ['TOPIC']


def delete(event, context):

    if type(event) is str:
        event = json.loads(event)

    id = event['pathParameters']['id']

    response = sns.publish(TopicArn=topic,
                           Message=json.dumps(
                               {'item_id': id}
                           ))

    return {
        'statusCode': 200
    }
