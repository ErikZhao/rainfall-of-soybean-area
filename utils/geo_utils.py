# coding=utf-8

import logging

from utils import log_utils
from config.geo_config import GEO_LOCATOR

__author__ = "linghanzhao"
__created__ = "10/23/16"

"""
File Description
"""

logging.basicConfig()
logger = logging.getLogger(__name__)


def get_location_from_geopy(location=None):
    """This function search location's lat and lon from geopy

    :param location:
    :return:
    """
    if not location:
        log_utils.log_msg_error(logger=logger, key='GEOUTILS0001', msg='Missing location arg',
                                values={"Location not found": location})
        return None, None

    lat = None
    lon = None

    try:
        # get geocode object
        location_info = GEO_LOCATOR.geocode(location)
        lat = location_info.latitude
        lon = location_info.longitude
    except Exception as e:
        log_utils.log_msg_error(logger=logger, key='GEOUTILS0002', msg='Get geo code Error',
                                values={"Location not found": location}, exception=e)

    return lat, lon

