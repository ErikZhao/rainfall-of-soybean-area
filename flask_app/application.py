# coding=utf-8

import flask
import datetime
from flask import Flask, request

from mongo import mongoAPI
from darksky import darkskyAPI


__author__ = "linghanzhao"
__created__ = "10/24/16"

"""
File Description
"""

application = Flask(__name__)

db = mongoAPI.get_db()
collections = mongoAPI.get_collections(db)

# @application.route("/")
# def hello():
#     return "hello world"

@application.route("/", methods=['GET', 'POST'])
def get_parameters():
    filter = request.args.get('filter')
    result = []
    if filter:
        if filter.lower() == 'state':
            data = mongoAPI.get_all_document(collections["soybeans_state"])
            for each in data:
                lat = each['geo_location']['lat']
                lon = each['geo_location']['lon']
                state_name = each['state_name']
                today = datetime.datetime.now().date()

                weather_document = mongoAPI.get_one_document(collections["weathers"], {'date': str(today), 'state_name': state_name})
                if weather_document:
                    rain_fall = weather_document['rain_fall']
                else:
                    rain_fall = darkskyAPI.get_today_rain_fall(lat, lon)
                    mongoAPI.insert_one_document(collections["weathers"], {'date': str(today), 'state_name': state_name, 'rain_fall': rain_fall})

                result.append((each['state_name'], rain_fall))
        elif filter.lower() == 'county':
            data = mongoAPI.get_all_document(collections["soybeans_county"])
            for each in data:
                lat = each['geo_location']['lat']
                lon = each['geo_location']['lon']
                # rain_fall = darkskyAPI.get_today_rain_fall(lat, lon)
                result.append((each['county_name'], 1))
        else:
            pass

    return flask.render_template('index.html', result=result)


if __name__ == "__main__":
    application.run()