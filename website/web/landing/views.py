from . import landing

import os
import datetime
import flask
import logging
import json
#import sqlite3

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

# import flask_login
# current_user = flask_login.current_user

MQTT_DB = 'web/db/mqtt.json'
IORA_DB = 'web/db/iora.json'
FAKE_DB = 'web/db/fake.json'

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

@landing.route("/chart")
def chart():
    legend = 'Temperatures'
    temperatures = [23.7, 23.4, 23.8, 23.8, 18.7, 15.2,
                    11.8, 08.7, 08.2, 18.3, 10.5, 15.7,
                    20.2, 21.4, 21.2, 20.9, 21.3, 21.1]
    times = ['12:00PM', '12:10PM', '12:20PM', '12:30PM', '12:40PM', '12:50PM',
             '1:00PM', '1:10PM', '1:20PM', '1:30PM', '1:40PM', '1:50PM',
             '2:00PM', '2:10PM', '2:20PM', '2:30PM', '2:40PM', '2:50PM']
    return render_template('chart.html', values=temperatures, labels=times, legend=legend)

@landing.route('/hub/{<string:meth>}')
    
@landing.route('/hub', methods=['GET'])
@landing.route('/hub/<string:meth>', methods=['GET'])
def hub(meth="none"):
    
    # Get data from database
    if (meth.lower() == "iora"):
        futair_data = json.load(open(IORA_DB))
    
    elif (meth.lower() == "mqtt"):
        futair_data = json.load(open(MQTT_DB))
    else:
        futair_data = json.load(open(FAKE_DB))
    #try:
    #    # Get data from database
    #    if (meth.lower() == "iora"):
    #        futair_data = json.load(open(IORA_DB))
    #    
    #    elif (meth.lower() == "mqtt"):
    #        futair_data = json.load(open(MQTT_DB))
    #    else:
    #        futair_data = json.load(open(FAKE_DB))
    #except:
    #    futair_data = json.load(open(FAKE_DB))
    
    # NO2: 45-70, 53 is standard
    # CO: 
    # Fake data for testing
    
    return render_template('hub.html', page_title='Data Hub', data = futair_data)
