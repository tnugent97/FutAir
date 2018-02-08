from . import landing

import os
import datetime
import flask
import logging

from flask import (
    #Flask,
    abort,
    redirect,
    render_template,
    request,
    url_for,
    Response,
    session
)

import flask_login
current_user = flask_login.current_user

logger = logging.getLogger("web.landing.views")

def make_error_response(description):
    return flask.Response(
        json.dumps({"status": "error", "message": description}),
        status=400,
        content_type="application/json")



@landing.route('/', methods=['GET'])
@landing.route('/home', methods=['GET'])
@landing.route('/home', methods=['GET'])
def index():
    return render_template('index.html', page_title='Home')
    

@landing.route('/hub', methods=['GET'])
def hub():
    # Get data from database
     
    # Fake data for teesting
    airheads = {
        "uniqueid1":
            {"location":{"lat":51.4988,"lng":-0.1749},
             "payload":{
                "temp":5, # degrees centigrade
                "humidity":0.62, # Percentage
                "CO conc.":10,
                "NO2 conc.":50, # in microgrammes per metre cubed (ug/m3)
                "pressure":1017.5 # hPa
                }
            },
        "uniqueid2":
            {"location":{"lat":51.5073,"lng":-0.1657},
             "payload":{
                "temp":5, # degrees centigrade
                "humidity":0.62, # Percentage
                "CO conc.":8,
                "NO2 conc.":40, # in microgrammes per metre cubed (ug/m3)
                "pressure":1012.5 # hPa
                }
            },
        }
    return render_template('hub.html', page_title='Data Hub', data = airheads)
