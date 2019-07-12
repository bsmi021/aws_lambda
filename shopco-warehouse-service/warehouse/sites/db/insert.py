import os
import logging
import json
from datetime import datetime

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DECIMAL, Integer, DateTime
from sqlalchemy.orm import sessionmaker

from warehouse.models import Site

logger = logging.getLogger()
logger.setLevel(logging.INFO)


db_host = os.environ.get('host')
db_port = os.environ.get('port')
db_user = os.environ.get('user')
db_pass = os.environ.get('pass')
db_name = os.environ.get('db')

db_uri = f'postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

db_engine = create_engine(db_uri)
Session = sessionmaker(bind=db_engine)
session = Session()

logger.info(f'Connected to the {db_name} database.')


def insert(event, context):
    """Inserts a Site record into the database

    Arguments:
        event {object} -- Contains the payload
        context {object} -- Contains the Lambda Context information
    """
    for record in event['Records']:
        data = json.loads(record['Sns']['Message'])

        site = Site(site_id=data['site_id'], name=data['name'],
                    zip_code=data['zip_code'], type_id=data['type_id'])
        site.created_at = datetime.utcnow()
        site.updated_at = datetime.utcnow()
        site.is_deleted = False
        try:
            # add the order to the session
            session.add(site)
            session.commit()

            logger.info(site)
        except Exception as ex:
            logger.error('Issue in submitting site -- %s' % site)
            logger.error(ex)
