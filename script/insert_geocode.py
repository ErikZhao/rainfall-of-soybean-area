# coding=utf-8

import logging

from mongo import mongoAPI
from utils import log_utils, geo_utils

__author__ = "linghanzhao"
__created__ = "10/23/16"

"""
File Description
"""

logging.basicConfig()
logger = logging.getLogger(__name__)

db = mongoAPI.get_db()
collections = mongoAPI.get_collections(db)

def insert_geo_to_mongo(collection):
    """This function inserts geocode to soybean collection

    :param collection:
    :return:
    """
    if not collection:
        log_utils.log_msg_error(logger=logger, key='INSERTGEOCODE0001', msg='Collection is None')
        return None

    cursor = collection.find()
    count = 1

    for each in cursor:
        location = each['location_desc']
        id = each['_id']
        lat, lon = geo_utils.get_location_from_geopy(location)

        collection.update({'_id': id}, {"$set" :{'geo_location': {'lat': lat, 'lon': lon}}}, True)

        print count
        count += 1


# insert_geo_to_mongo(collections['soybeans_state'])
