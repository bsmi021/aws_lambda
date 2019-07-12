import os
import logging
import json
from datetime import datetime

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DECIMAL, Integer, DateTime
from sqlalchemy.orm import sessionmaker

from warehouse.models import Site, SiteTypes

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


def get_sites():
    sites = session.query(Site).all()

    return sites


def list(event, context):
    """Retrieves a single Site record from the database.

    Arguments:
        event {object} -- Event payload
        context {object} -- Lambda Context

    """

    if type(event) is str:
        event = json.loads(event)

    sites = get_sites()

    if sites is None:
        raise Exception('Not found')

    response_body = []

    for site in sites:
        site = {
            'id': site.site_id,
            'name': site.name,
            'zip_code': site.zip_code,
            'type_id': site.type_id,
            'type': SiteTypes[site.type_id],
            'created_at': str(site.created_at),
            'updated_at': str(site.updated_at)
        }
        response_body.append(site)

    response = {
        'statusCode': 200,
        'body': json.dumps(response_body)
    }

    return response
