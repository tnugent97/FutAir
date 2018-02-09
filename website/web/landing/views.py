from . import landing

import os
import datetime
import flask
import logging
import sqlite3

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


DATABASE = 'web/db/history.db'
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    return db
        
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(values=(1,"hi", 0.4,0.3,43,0.65,0.2,0.3,100,datetime.datetime.now(),datetime.datetime.now())):
    # id,nickname,lat,lng,temp,humidity,CO_conc,NO2,pressure,device_time,created
    cur = get_db().cursor()
    cur.execute('INSERT INTO datapoints VALUES (?,?,?,?,?,?,?,?,?,?,?)', values)
    
@landing.route('/hub', methods=['GET'])
def hub():
    # Get data from database
    # insert_db()
    #data = query_db('SELECT * FROM datapoints')
    
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
