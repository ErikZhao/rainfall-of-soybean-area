# coding=utf-8

import flask
from flask import Flask, request
# from mongo import mongoAPI

__author__ = "linghanzhao"
__created__ = "10/24/16"

"""
File Description
"""

application = Flask(__name__)

# db = mongoAPI.get_db()
# collections = mongoAPI.get_collections(db)

# @application.route("/")
# def hello():
#     return "hello world"

@application.route("/", methods=['GET', 'POST'])
def get_parameters():
    filter = request.args.get('filter')

    return flask.render_template('index.html', result=filter)


if __name__ == "__main__":
    application.run()