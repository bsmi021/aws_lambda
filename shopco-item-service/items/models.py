import os
from enum import Enum
import boto3
from datetime import datetime
from uuid import uuid4


class ItemModel:
    """
    A product in the Shopco System
    """
    def __init__(self,id, sku, name, description, price, product_brand_id, createdAt = str(datetime.utcnow()), modifiedAt = str(datetime.utcnow()), discontinued = False ):
        self.id = id
        self.sku = sku
        self.name = name
        self.description = description
        self.price = price
        self.product_brand_id = product_brand_id
        self.discontinued = discontinued
        self.createdAt = createdAt
        self.modifedAt = modifiedAt


    def create()    

    
