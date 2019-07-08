import os
from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

aws_region = os.environ['REGION']

class CustomerModel(Model):
    class Meta:
        table_name = os.environ['DYNAMODB_TABLE']
        if 'ENV' in os.environ:
            host = 'http://localhost:8000'
        else:
            region = aws_region
            host = f'https://dynamodb.{aws_region}.amazonaws.com'

    id = UnicodeAttribute(hash_key=True, null=False)
    first_name=UnicodeAttribute(null=False)
    last_name=UnicodeAttribute(null=False)

    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())
    updatedAt = UTCDateTimeAttribute(null=False)

    def save(self, conditional_operator=None, **expected_values):
        self.updatedAt = datetime.now()
        super(CustomerModel, self).save()

    def __iter__(self):
        for name, attr in self._get_attributes().items():
            yield name, attr.serialize(getattr(self,name))

    