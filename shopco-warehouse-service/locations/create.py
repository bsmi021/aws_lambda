import json
import logging
import uuid
import os

# condition to test if running locally
if 'ENV' in os.environ:
    from models import LocationModel
    from schema import validate_location_json
else:
    from locations.models import LocationModel
    from locations.schema import validate_lcoation_json


def create(event, context):

    data = json.loads(event['body'])

    if not validate_location_json(data):
        raise Exception('Invalid content provided.')

    try:
        location = LocationModel(
            name=data['name'],
            street_1=data['street_1'],
            street_2=data.get('street_2', None),
            city=data['city'],
            state=data['state'],
            zip_code=data['zip_code'],
            country=data['country'],
            type_id=data['type_id']
        )

        location.save()

        response = {'statusCode': 200,
                    'body': json.dumps(dict(location))}
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

    print(os.environ['DYNAMODB_TABLE'])
    print(os.environ['ENV'])
    print(os.environ['REGION'])

    place = {
        'name': 'TestSite',
        'street_1': '1313 mockingbird ln',
        #'street_2': 'post box',
        'city': 'anytown',
        'state': 'ny',
        'zip_code': '11752',
        'country': 'us',
        'type_id': 3
    }

    payload = {
        'body': json.dumps(place)
    }

    location = create(payload, None)

    print(location)
