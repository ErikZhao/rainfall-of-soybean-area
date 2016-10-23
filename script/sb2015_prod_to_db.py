# coding=utf-8

import os
import json
import logging

from config import download_config
from download import download
from mongo import mongoAPI
from utils import log_utils

__author__ = "linghanzhao"
__created__ = "10/22/16"

"""
File Description: store soybean production to database
"""

logging.basicConfig()
logger = logging.getLogger(__name__)

SOYBEAN_COUNTY_URL = "https://quickstats.nass.usda.gov/api/api_GET/?key=657A7402-DF3A-3C12-A7D6-FFCC1DDE180D&format=json&year=2015&commodity_desc=SOYBEANS&statisticcat_desc=PRODUCTION&agg_level_desc=COUNTY&unit_desc=BU&prodn_practice_desc=ALL%20PRODUCTION%20PRACTICES&reference_period_desc=YEAR"
SOYBEAN_STATE_URL = "https://quickstats.nass.usda.gov/api/api_GET/?key=657A7402-DF3A-3C12-A7D6-FFCC1DDE180D&format=json&year=2015&commodity_desc=SOYBEANS&statisticcat_desc=PRODUCTION&agg_level_desc=STATE&unit_desc=BU&prodn_practice_desc=ALL%20PRODUCTION%20PRACTICES&reference_period_desc=YEAR"

db = mongoAPI.get_db()
collections = mongoAPI.get_collections(db)


def store_production_to_db(url, collection):
    """This function uses url to download json file and store them to related collection

    :param url:
    :param collection:
    :return:
    """
    if not url:
        log_utils.log_msg_error(logger=logger, key='SB2015PRODTODB0001', msg='URL is None')
        return None
    if not collection:
        log_utils.log_msg_error(logger=logger, key='SB2015PRODTODB0002', msg='Collection is None')
        return None

    # Download file
    try:
        filename = download.easy_downloader(url, download_config.HTTP_PROXY)
    except Exception as e:
        log_utils.log_msg_error(logger=logger, key='SB2015PRODTODB0003', msg='Download Error', exception=e)
        return None

    # Open file and store each info to database
    try:
        with open(filename, 'r') as f:
            d = json.load(f)
            f.close()
            for each in d['data']:
                mongoAPI.insert_one_document(collection, each)
    except Exception as e:
        log_utils.log_msg_error(logger=logger, key='SB2015PRODTODB0004', msg='Store to DB Error', exception=e)
        return None

    # Remove Downloaded File
    try:
        os.remove(filename)
    except Exception as e:
        log_utils.log_msg_error(logger=logger, key='SB2015PRODTODB0005', msg="Remove file Error", exception=e)

# store_production_to_db(SOYBEAN_COUNTY_URL, collections['soybeans_county'])
# store_production_to_db(SOYBEAN_STATE_URL, collections['soybeans_state'])
