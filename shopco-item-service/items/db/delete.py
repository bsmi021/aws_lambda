import os
import json
import boto3

import datetime as dt

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def delete(event, context):
    """This method will not actually delete the record, it will update the
        delete flag on the record in the table.

    Arguments:
        event {object} -- [description]
        context {object} -- [description]
    
    Returns:
        object -- [description]
    """

    if type(event) == str:
        event = json.loads(event)

    for record in event['Records']:
        data = json.loads(record['Sns']['Message'])

        item = table.get_item(
            Key={
                'id':data['id']
            }
        )

        if 'Item' in item:
            result = table.update_item(
                Key={ 'id': data['id']},
                ExpressionAttributeNames={
                    '#is_deleted': 'deleted'
                },
                ExpressionAttributeValues={
                    ':delete_flg': True,
                    ':updatedAt': str(dt.datetime.utcnow())
                },
                UpdateExpression='SET #is_deleted = :delete_flg, modifiedAt = :updatedAt',
                ReturnValues='ALL_NEW'
            )


    response = {
        'statusCode': 200
    }

    return response