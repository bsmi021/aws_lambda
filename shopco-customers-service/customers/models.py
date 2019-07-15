import os
from datetime import datetime

from pynamodb.attributes import (UnicodeAttribute,
                                 BooleanAttribute,
                                 UTCDateTimeAttribute,
                                 NumberAttribute,
                                 JSONAttribute,
                                 MapAttribute)
from pynamodb.models import Model

aws_region = os.environ['REGION']


class BaseModel(Model):
    def to_dict(self):
        rval = {}
        for key in self.attribute_values:
            rval[key] = self.__getattribute__(key)
        return rval

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


class Address(MapAttribute):
    street_1 = UnicodeAttribute()
    street_2 = UnicodeAttribute(null=True)
    city = UnicodeAttribute()
    state = UnicodeAttribute()
    zip_code = UnicodeAttribute()
    country = UnicodeAttribute()


class CustomerModel(BaseModel):
    class Meta:
        table_name = os.environ['DYNAMODB_TABLE']
        if 'ENV' in os.environ:
            host = 'http://localhost:8000'
        else:
            region = aws_region
            host = f'https://dynamodb.{aws_region}.amazonaws.com'

    id = UnicodeAttribute(hash_key=True, null=False)
    first_name = UnicodeAttribute(null=False)
    last_name = UnicodeAttribute(null=False)
    #address = Address()
    version = NumberAttribute(null=False)
    email_addr = UnicodeAttribute(null=False)
    phone_number = UnicodeAttribute(null=True)
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())
    updatedAt = UTCDateTimeAttribute(null=False)

    def save(self, conditional_operator=None, **expected_values):
        version = self.version
        if version is None:
            self.version = 1
        else:
            self.version = int(self.version) + 1
        self.updatedAt = datetime.now()
        super(CustomerModel, self).save()
