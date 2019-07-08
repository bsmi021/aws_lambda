import boto3
import json
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DECIMAL, Integer, DateTime
from sqlalchemy.orm import sessionmaker
import datetime as dt
from uuid import uuid4
import psycopg2
import os
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s: %(message)s')

# get environ vars
db_host = os.environ.get('host')
db_port = os.environ.get('port')
db_user = os.environ.get('user')
db_pass = os.environ.get('pass')
db_name = os.environ.get('db')
added_queue_name = os.environ.get('added_queue_name')

# postgress connection
db_uri = f'postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
Base = declarative_base()
db_engine = create_engine(db_uri)
logging.info(f'Connected to the {db_name} database.')
print('Connected')

# set connection to sqs
sqs = boto3.resource('sqs')
print(order_added_queue_name)
order_added_queue = sqs.get_queue_by_name(QueueName=added_queue_name)
logging.info(f"Connected to SQS - {added_queue_name}")


# class/table Brand/brands
class Brand(Base):
    __tablename__ = 'brands'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Brand(id={self.id}, name={self.name}, created_at={str(self.created_at)}, updated_at={str(self.updated_at)}>"

#TODO Add brand to DynamoDB
def add_brand_sqs(event, context):
    for record in event['Records']:
        print(record)
        body = json.loads(record['body'])
        name = body["name"]

        brand = Brand(id=brandId, )

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

def add_brand_db(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
