import json
import os
import logging

if 'ENV' in os.environ:
    from models import LocationModel
else:
    from locations.models import LocationModel

logger = logging.getLogger()


def update(event, context):
    id = event['pathParameters']['id']

    location = LocationModel.get(id)

    if location is None:
        raise Exception('Not found')
        return
    
    data = json.loads(event['body'])

    try:
        location.name = data.get('name', location.name)
        location.street_1 = data.get('street_1', location.street_1)
        location.street_2 = data.get('street_2', location.street_2)
        location.city = data.get('city', location.city)
        location.state = data.get('state', location.state)
        location.zip_code = data.get('zip_code', location.zip_code)
        location.type_id = data.get('type_id', location.type_id)

        location.save()

        response = {
            'statusCode': 200,
            'body': json.dumps(dict(location))
        }
    except Exception as ex:
        response = {'statusCode': 500,
                    'body': json.dumps({
                        'errorMessage': 'There was a problem saving'
                    })}

    return response

if __name__ == "__main__":
    # Tests the method against a local DynamoDb, pull local docker version:
    # docker run --rm -p 8000:8000 amazon/dynamodb-local:latest
    # requires the following env variables
    # - DYNAMODB_TABLE=<TABLENAME>
    # - REGION=<WHATEVER>
    # - ENV=1

    place = {
        'name': 'TestSite',
        'street_1': '1313 mockingbird ln',
        'street_2': 'New Post Box',
        'city': 'anytown',
        'state': 'ny',
        'zip_code': '11752',
        'country': 'us',
        'type_id': 3
    }

    payload = {
        'pathParameters': {
            'id': '3f600e2a-3e5e-463a-8563-e7db2d2091e2'
        },
        'body': json.dumps(place)
    }

    location = update(payload, None)

    print(location)
