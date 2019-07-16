import os
import json
from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute,
                                 UTCDateTimeAttribute,
                                 UnicodeSetAttribute,
                                 NumberAttribute,
                                 MapAttribute,
                                 BooleanAttribute,
                                 ListAttribute)
from uuid import uuid4
from datetime import datetime

aws_region = os.getenv('REGION', 'none')


class BaseModel(Model):
    created_at = UTCDateTimeAttribute(default=datetime.utcnow())
    updated_at = UTCDateTimeAttribute(default=datetime.utcnow())

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            if isinstance(attr, MapAttribute):
                if getattr(self, name):
                    yield name, getattr(self, name).as_dict()
            elif isinstance(attr, UTCDateTimeAttribute):
                if getattr(self, name):
                    yield name, attr.serialize(getattr(self, name))
            elif isinstance(attr, NumberAttribute):
                # if numeric return value as is.
                yield name, getattr(self, name)
            else:
                yield name, attr.serialize(getattr(self, name))


LocationTypes = {
    1: 'Distribution Center',
    2: 'Store',
    3: 'Forward Shipping',
    4: 'Seasonal'
}


class LocationModel(BaseModel):
    class Meta:
        table_name = os.environ['DYNAMODB_TABLE']
        if 'ENV' in os.environ:
            host = f"http://localhost:8000"
        else:
            region = aws_region
            host = f'https://dynamodb.{aws_region}.amazonaws.com'

    id = UnicodeAttribute(default=str(uuid4()), hash_key=True)

    name = UnicodeAttribute()
    street_1 = UnicodeAttribute()
    street_2 = UnicodeAttribute(null=True)
    city = UnicodeAttribute()
    state = UnicodeAttribute()
    zip_code = UnicodeAttribute()
    country = UnicodeAttribute(default='US')
    type_id = NumberAttribute()
    loc_type = UnicodeAttribute(default='')
    is_deleted = BooleanAttribute(default=False)

    def save(self, conditional_operator=None, **excpected_values):
        self.loc_type = LocationTypes.get(self.type_id, 1)

        self.updated_at = datetime.utcnow()
        super(LocationModel, self).save()

    def __repr__(self):
        return f'<Site "id":{self.id}, "name":{self.name}, "type":{self.loc_type}/>'


if __name__ == "__main__":
    # Tests the model against a local DynamoDb, pull local docker version:
    # docker run --rm -p 8000:8000 amazon/dynamodb-local:latest

    os.environ['REGION'] = 'us-east-2'
    os.environ['DYNAMODB_TABLE'] = 'sites'
    os.environ['ENV'] = "1"

    if not LocationModel.exists():
        LocationModel.create_table(read_capacity_units=1,
                                   write_capacity_units=1,
                                   wait=True)

    location = LocationModel(name="Test Site",
                             street_1="Test Street 1",
                             street_2="Test Street 2",
                             city="Test City",
                             state="Test State",
                             zip_code="Test Zip",
                             type_id=1)
    location.save()

    print(json.dumps(dict(location)))

    location.type_id = 2
    location.save()

    print(json.dumps(dict(location)))
