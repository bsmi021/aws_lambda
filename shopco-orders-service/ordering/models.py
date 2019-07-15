import os
from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute,
                                 UTCDateTimeAttribute,
                                 UnicodeSetAttribute,
                                 NumberAttribute,
                                 MapAttribute,
                                 ListAttribute)
from uuid import uuid4
from datetime import datetime

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


class OrderAddress(MapAttribute):
    street_1 = UnicodeAttribute()
    street_2 = UnicodeAttribute(null=True)
    city = UnicodeAttribute()
    state = UnicodeAttribute()
    zip_code = UnicodeAttribute()
    country = UnicodeAttribute()


class Buyer(MapAttribute):
    first_name = UnicodeAttribute()
    last_name = UnicodeAttribute()
    email_address = UnicodeAttribute()
    phone_number = UnicodeAttribute()


class PaymentMethod(MapAttribute):
    card_number = UnicodeAttribute()
    expiration = UnicodeAttribute()
    ccv = NumberAttribute()
    card_type = UnicodeAttribute()


class OrderItem(MapAttribute):
    product_id = UnicodeAttribute(attr_name='id')
    product_name = UnicodeAttribute(attr_name='name')
    unit_price = NumberAttribute(attr_name='price')
    quantity = NumberAttribute()
    line_total = NumberAttribute(default=0)

    def set_line_total(self):
        self.line_total = self.unit_price * self.quantity


class Order(BaseModel):
    class Meta:
        table_name = os.environ['DYNAMODB_TABLE']
        if 'ENV' in os.environ['DYNAMODB_TABLE']:
            host = "http://localhost:8000"
        else:
            region = aws_region
            host = f'https://dynamodb.{aws_region}.amazonaws.com'

    id = UnicodeAttribute(default=str(uuid4()), hash_key=True)

    customer_id = UnicodeAttribute()

    buyer = Buyer()
    bill_addr = OrderAddress()
    ship_addr = OrderAddress()
    order_dt = UTCDateTimeAttribute(default=datetime.utcnow())
    line_items = ListAttribute(of=OrderItem)
    status = UnicodeAttribute()
    pay_method = PaymentMethod()
    order_total = NumberAttribute(default=0)

    def __repr__(self):
        return f"<Order 'id':{self.id}, 'order_date':{self.order_dt}>"
