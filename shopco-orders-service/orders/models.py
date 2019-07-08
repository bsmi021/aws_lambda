from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DECIMAL, Integer, DateTime

Base = declarative_base()

# class/table Order/order
class Order(Base):
    __schema__ = 'public'
    __tablename__ = 'order'

    id = Column(String, primary_key=True)
    order_date = Column(DateTime)
    order_amount = Column(DECIMAL)

    def __repr__(self):
        return "<Order(id='%s', order_date='%s', order_amt=%s>" % (self.id, self.order_date, self.order_amount)
