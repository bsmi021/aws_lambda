from jsonschema import validate

location_schema = {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://example.com/root.json",
    "type": "object",
    "title": "The Root Schema",
    "required": [
        "city",
        "country",
        "name",
        "state",
        "street_1",
        "type_id",
        "zip_code"
    ],
    "properties": {
        "city": {
            "$id": "#/properties/city",
            "type": "string",
            "title": "The City Schema",
            "default": "",
            "examples": [
                "Test City"
            ],
            "pattern": "^(.*)$"
        },
        "country": {
            "$id": "#/properties/country",
            "type": "string",
            "title": "The Country Schema",
            "default": "US",
            "examples": [
                "US"
            ],
            "pattern": "^(.*)$"
        },
        "name": {
            "$id": "#/properties/name",
            "type": "string",
            "title": "The Name Schema",
            "default": "",
            "examples": [
                "Test Site"
            ],
            "pattern": "^(.*)$"
        },
        "state": {
            "$id": "#/properties/state",
            "type": "string",
            "title": "The State Schema",
            "default": "",
            "examples": [
                "Test State"
            ],
            "pattern": "^(.*)$"
        },
        "street_1": {
            "$id": "#/properties/street_1",
            "type": "string",
            "title": "The Street_1 Schema",
            "default": "",
            "examples": [
                "Test Street 1"
            ],
            "pattern": "^(.*)$"
        },
        "street_2": {
            "$id": "#/properties/street_2",
            "type": "string",
            "title": "The Street_2 Schema",
            "default": "",
            "examples": [
                "Test Street 2"
            ],
            "pattern": "^(.*)$"
        },
        "type_id": {
            "$id": "#/properties/type_id",
            "type": "integer",
            "title": "The Type_id Schema",
            "default": 0,
            "examples": [
                2
            ]
        },
        "zip_code": {
            "$id": "#/properties/zip_code",
            "type": "string",
            "title": "The Zip_code Schema",
            "default": "",
            "examples": [
                "Test Zip"
            ],
            "pattern": "^(.*)$"
        }
    }
}


def validate_location_json(payload):
    try:
        validate(payload, schema=location_schema)
        return True
    except:
        return False
