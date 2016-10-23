# coding=utf-8


import logging
import uuid
import os
import urllib

from utils import log_utils
from config import download_config

__author__ = "linghanzhao"
__created__ = "10/23/16"

"""
File Description
"""

logging.basicConfig()
logger = logging.getLogger(__name__)


def easy_downloader(url=None, proxy=None):
    """This function is a fast downloader, using Default header settings.

    Easy Downloader, default HTTPS proxy.

    :param url: destination url
    :type url: str
    :param proxy: proxy, default HTTPS proxy
    :type proxy: dict
    :return: str -- downloaded File Path aka. file name

    """
    if url is None or url == "":
        log_utils.log_msg_warning(logger=logger, key='DOWNLOADER0001', msg="Url is None")
        return None

    file_name = uuid.uuid4().__str__().split('-')[4] + '_' + url.split('/')[-1].split('?')[0]

    orig_url = url
    try:
        url = url.encode('utf-8', 'ignore')
    except Exception as e:
        log_utils.log_msg_error(logger=logger, key='DOWNLOADER0002', msg="encode url failure",
                                values={"URL": url}, exception=e)
        url = orig_url

    try:
        if not proxy:
            proxy = download_config.HTTPS_PROXY
        filehandler = urllib.urlopen(url, proxies=proxy).read()
    except Exception as e:
        log_utils.log_msg_error(logger=logger, key='DOWNLOADER0003', msg="open url failure",
                                values={"URL": url}, exception=e)
        filehandler = None

    log_utils.log_msg_debug(logger=logger, key='DOWNLOADER0004', values={'proxy': proxy})

    try:
        with open(file_name, 'wb') as f:
            f.write(filehandler)
        f.close()
    except Exception as e:
        log_utils.log_msg_error(logger=logger, key='DOWNLOADER0005', msg="Fail to Write File",
                                values={"URL": url}, exception=e)
        os.remove(file_name)
        return None
    log_utils.log_msg_debug(logger=logger, key='DOWNLOADER0006', msg="Downloader Succeed", values={"URL": url})

    return file_name
