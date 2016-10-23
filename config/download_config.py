# coding=utf-8

import os

__author__ = "linghanzhao"
__created__ = "10/23/16"

"""
File Description
"""

###########################
# Proxy Config
###########################

HTTPS_PROXY_URI = os.environ.get("HTTPS_PROXY_URI", 'https://10.1.10.210:3128')
HTTPS_PROXY = {'https': HTTPS_PROXY_URI}

HTTP_PROXY_URI = os.environ.get("HTTP_PROXY_URI", 'http://10.1.10.210:3128')
HTTP_PROXY = {'http': HTTP_PROXY_URI}