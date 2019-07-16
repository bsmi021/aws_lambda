import os
import json
import logging

if 'ENV' in os.environ:
    from models import LocationModel
else:
    from locations.models import LocationModel

logger = logging.getLogger()


def list(event, context):
    results = LocationModel.scan()

    return {
        'statusCode': 200,
        'body': json.dumps({'locations': [dict(result) for result in results]})
    }


if __name__ == "__main__":
    # Tests the method against a local DynamoDb, pull local docker version:
    # docker run --rm -p 8000:8000 amazon/dynamodb-local:latest
    # requires the following env variables
    # - DYNAMODB_TABLE=<TABLENAME>
    # - REGION=<WHATEVER>
    # - ENV=1

    response = list(None, None)

    print(response)
