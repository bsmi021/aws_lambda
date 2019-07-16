import os
import json
import logging

if 'ENV' in os.environ:
    from models import LocationModel
else:
    from locations.models import LocationModel

logger = logging.getLogger()


def get(event, context):
    id = event['pathParameters']['id']

    try:
        location = LocationModel.get(id)

        response = {
            'statusCode': 200,
            'body': json.dumps(dict(location))
        }
    except Exception as ex:
        response = {'statusCode': 500,
                    'body': json.dumps({
                        'errorMessage': 'There was a problem deleting'
                    })}

    return response


if __name__ == "__main__":
    # Tests the method against a local DynamoDb, pull local docker version:
    # docker run --rm -p 8000:8000 amazon/dynamodb-local:latest
    # requires the following env variables
    # - DYNAMODB_TABLE=<TABLENAME>
    # - REGION=<WHATEVER>
    # - ENV=1

    payload = {
        'pathParameters': {
            'id': '3f600e2a-3e5e-463a-8563-e7db2d2091e2'
        }
    }

    response = get(payload, None)

    print(response)
