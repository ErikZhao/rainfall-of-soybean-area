# coding=utf-8

import logging
import datetime

import forecastio

from config import darksky_config
from utils import log_utils


__author__ = "linghanzhao"
__created__ = "10/23/16"

"""
File Description
"""

logging.basicConfig()
logger = logging.getLogger(__name__)


def get_today_rain_fall(lat, lon, time=datetime.datetime.now()):
    """This function calls darkSky API to get daily rain fall from latitude and longitude

    :param lat: latitude
    :param lon: longitude
    :param time:
    :return:
    """
    if not lat or not lon:
        log_utils.log_msg_error(logger=logger, key='DARKSKYAPI0001', msg='lat or lon is None')
        return None

    try:
        forecast = forecastio.load_forecast(darksky_config.DARKSKY_API_KEY, lat, lon, time=time)
        rain_fall = forecast.currently().precipIntensity
    except Exception as e:
        log_utils.log_msg_error(logger=logger, key='DARKSKYAPI0002', msg='Get today rainfall from DarkSky API Error',
                                exception=e)
        return None

    return rain_fall


# byDay = forecast.daily()
#
# for dailyData in byDay.data:
#     print dailyData
#     print dailyData.precipIntensity

# 40.0583238, -74.4056612

# print get_today_rain_fall(40.0583238, -74.4056612)