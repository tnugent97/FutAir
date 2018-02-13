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
    
@landing.route('/hub', methods=['GET'])
@landing.route('/hub/{<string:meth>}', methods=['GET'])
def hub(meth="none"):
    try:
        # Get data from database
        if (meth.lower() == "iora"):
            futair_data = json.load(open(IORA_DB))
        
        else:
            futair_data = json.load(open(MQTT_DB))
    except:
        futair_data = {
            "uniqueid1":
                {"location":{"lat":51.4988,"lng":-0.1749},
                 "payload":{
                    "temp":5, # degrees centigrade
                    "humidity":0.62, # Percentage
                    "CO":7,
                    "NO2":50, # in microgrammes per metre cubed (ug/m3)
                    "pressure":1017.5 # hPa
                    }
                },
            "uniqueid2":
                {"location":{"lat":51.5073,"lng":-0.1657},
                 "payload":{
                    "temp":5, # degrees centigrade
                    "humidity":0.62, # Percentage
                    "CO":5,
                    "NO2":40, # in microgrammes per metre cubed (ug/m3)
                    "pressure":1012.5 # hPa
                    }
                },
            }
    
    # NO2: 45-70, 53 is standard
    # CO: 
    # Fake data for teesting
    
    return render_template('hub.html', page_title='Data Hub', data = futair_data)


#DATABASE = 'web/db/history.db'
#def make_dicts(cursor, row):
#    return dict((cursor.description[idx][0], value)
#                for idx, value in enumerate(row))
#def get_db():
#    db = sqlite3.connect(DATABASE)
#    db.row_factory = make_dicts
#    return db
#        
#def query_db(query, args=(), one=False):
#    cur = get_db().execute(query, args)
#    rv = cur.fetchall()
#    cur.close()
#    return (rv[0] if rv else None) if one else rv
#
#def insert_db(values=(1,"hi", 0.4,0.3,43,0.65,0.2,0.3,100,datetime.datetime.now(),datetime.datetime.now())):
#    # id,nickname,lat,lng,temp,humidity,CO_conc,NO2,pressure,device_time,created
#    cur = get_db().cursor()
#    cur.execute('INSERT INTO datapoints VALUES (?,?,?,?,?,?,?,?,?,?,?)', values)
