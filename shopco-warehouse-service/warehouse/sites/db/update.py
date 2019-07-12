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


def update(event, context):
    """Updates a Site record in the database

    Arguments:
        event {object} -- Contains the payload
        context {object} -- Contains Lambda Context Information
    """

    for record in event['Records']:
        data = json.loads(record['Sns']['Message'])

        try:
            site = session.query(Site).filter(
                Site.site_id == data['site_id']).first()

            if site is None:
                raise Exception('Site could not be found')

            site.name = data.get('name', site.name)
            site.zip_code = data.get('zip_code', site.zip_code)
            site.type_id = data.get('type_id', site.type_id)
            site.updated_at = datetime.utcnow()

            session.add(site)
            session.commit()

            logger.info(site)
        except Exception as ex:
            logger.error('Issue in updating site -- %s' % site)
            logger.error(ex)
