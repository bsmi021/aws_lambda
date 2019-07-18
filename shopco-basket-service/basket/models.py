import os
import json
from decimal import Decimal

from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute,
                                 UTCDateTimeAttribute,
                                 UnicodeSetAttribute,
                                 NumberAttribute,
                                 MapAttribute,
                                 ListAttribute
                                 )
from uuid import uuid4
from datetime import datetime

if 'ENV' in os.environ:
    from utils import DecimalEncoder
else:
    from basket.utils import DecimalEncoder

aws_region = os.environ['REGION']
dynamodb_table = os.environ['DYNAMODB_TABLE']


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


class Basket(BaseModel):
    class Meta:
        table_name = dynamodb_table
        if 'ENV' in os.environ:
            host = "http://localhost:8000"
        else:
            region = aws_region
            host = f"https://dynamodb.{aws_region}.amazonaws.com"

    customer_id = UnicodeAttribute(hash_key=True)
    product_id = UnicodeAttribute(range_key=True)
    price = NumberAttribute()
    quantity = NumberAttribute()
    line_total = NumberAttribute(default=0)

    def save(self, conditional_operator=None, **expected_values):
        self.line_total = self.quantity * self.price
        self.updated_at = datetime.utcnow()

        super(Basket, self).save()

    def delete(self):
        super(Basket, self).delete()

    def body(self):
        return json.dumps(dict(self), cls=DecimalEncoder)


if __name__ == "__main__":
    # Tests the model against a local DynamoDB
    # docker run --rm -p 8000:8000 amazon/dynamodb-local:latest

    if not Basket.exists():
        Basket.create_table(read_capacity_units=100,
                            write_capacity_units=100, wait=True)

    customer_id = str(uuid4())
    basket = Basket(customer_id=customer_id,
                    product_id="1", price=10.99, quantity=1)
    basket.save()

    for x in range(2, 5):
        Basket(customer_id=customer_id, product_id=str(x),
               price=29.99, quantity=1).save()

    print(basket.body())

    for item in Basket.query(customer_id):
        print(item.body())

    basket.delete()

    print()
    print('Check to see if the basket has the item')
    for item in Basket.query(customer_id):
        print(item.body())

    basket2 = Basket.get(customer_id, "2")

    print()
    print(basket2.body())
