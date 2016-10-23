# coding=utf-8


import logging
import ujson as json

logging.basicConfig()
my_logger = logging.getLogger(__name__)

__author__ = "linghanzhao"
__created__ = "10/23/16"

"""
File Description
"""


def log_msg_info(logger=None, key=None, msg=None, values=None, exception=None):
    if logger is None:
        logger.info(get_log_msg(key=key, msg=msg, values=values, exception=exception))
    else:
        my_logger.info(get_log_msg(key=key, msg=msg, values=values, exception=exception))


def log_msg_warning(logger=None, key=None, msg=None, values=None, exception=None):
    logger.warning(get_log_msg(key=key, msg=msg, values=values, exception=exception))


def log_msg_debug(logger=None, key=None, msg=None, values=None, exception=None):
    if logger is not None:
        logger.debug(get_log_msg(key=key, msg=msg, values=values, exception=exception))
    else:
        my_logger.debug(get_log_msg(key=key, msg=msg, values=values, exception=exception))


def log_msg_error(logger=None, key=None, msg=None, values=None, exception=None):
    if logger is not None:
        logger.error(get_log_msg(key=key, msg=msg, values=values, exception=exception))
    else:
        my_logger.error(get_log_msg(key=key, msg=msg, values=values, exception=exception))


def get_log_msg(key=None, msg=None, values=None, exception=None):
    try:
        msg = json.dumps({
            'OFO_JSON': '1.0',
            'elastic': "%s:%s:%s" % (True, "LOGSTASH_HOST", 5100),
            'build': "0",
            'branch': "",
            'key': key,
            'msg': msg,
            'values': values,
            'build_number': "0",
            'exception': str(exception)
        })
    except Exception as e:
        log_msg_error(key="LOGUTIL1", msg="GET LOG MSG failed!", values={"key": key, "msg": msg}, exception=e)
        return ""
    return msg
