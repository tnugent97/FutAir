from . import landing

import os
import datetime
import flask
import logging
import json
import random
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
LORA_DB = 'web/db/lora.json'
FAKE_DB = 'web/db/fake.json'

logger = logging.getLogger("web.landing.views")

def make_error_response(description):
    return flask.Response(
        json.dumps({"status": "error", "message": description}),
        status=400,
        content_type="application/json")

def generate_fake_json(fname='test.json'):
    # centre: lat: 51.4988, lng: -0.1667
    data = {}
    for i in range(3000):
        #lat = 51.442687 + (float(random.randint(0,25000))/100000.0) # from -0.310859 to -0.058149
        #lng = -0.283707 + (float(random.randint(0,50000))/100000.0) # from 51.433696 to 51.567723
        lat = random.gauss(51.4988,0.27)
        lng = random.gauss(-0.1667,0.27)
        bottom= 51.466503
        top= 51.520369
        left= -0.192333
        right= -0.059810
        if lat < 50.9:
            lat = 51.442687 + (float(random.randint(0,25000))/100000.0)
        
        temp = float(random.randint(500,1700))/100.0
        humidity = float(random.randint(40,80))/100.0
        CO = random.randint(1,6)
        NO2 = float(random.randint(320,600))/10.0
        if (lat > bottom) and (lat < top) and (lng > left) and (lng < right):
            CO   += random.randint(1,2)
            NO2 += random.randint(0,20)  
        pressure = 99500 + float(random.randint(10,5000))/10.0
        data[i] = {
                    "location":{"lat":lat,"lng":lng},
                    "payload":{
                        "temp":temp,
                        "humidity":humidity,
                        "CO":CO,
                        "NO2":NO2, 
                        "pressure":pressure
                    }
                }
    with open('web/db/{}'.format(fname), 'w') as outfile:
        json.dump(data, outfile)
    return
    
@landing.route('/fake/<string:fname>', methods=['GET'])
@landing.route('/fake', methods=['GET'])
def gen_fake_json(fname='test.json'):
    generate_fake_json('test.json')
    return redirect(url_for('landing.hub'), code=302)
    
@landing.route('/', methods=['GET'])
@landing.route('/home', methods=['GET'])
@landing.route('/home', methods=['GET'])
def index():
    return render_template('index.html', page_title='Home')

@landing.route("/chart", methods=['GET'])
@landing.route("/chart/<string:idn>", methods=['GET'])
@landing.route("/chart/<string:idn>/<string:meth>", methods=['GET'])
def chart(idn=None,meth="mqtt"):
    times = []
    temperatures = []
    legend = 'Temperatures'
    
    if meth=="lora":
        data = json.load(open(LORA_DB))
    else:
        data = json.load(open(MQTT_DB))
    if idn is not None and idn in data:
        sensor_i = data.get(idn)
        for x in sensor_i:
            print x["time"]
            times.append(x["time"])
            temperatures.append(x["temp"])
    else:
        temperatures = [23.7, 23.4, 23.8, 23.8, 18.7, 15.2,
                    11.8, 08.7, 08.2, 18.3, 10.5, 15.7,
                    20.2, 21.4, 21.2, 20.9, 21.3, 21.1]
        times = ["12:00PM", "12:10PM", "12:20PM", "12:30PM", "12:40PM", "12:50PM",
                "1:00PM", "1:10PM", "1:20PM", "1:30PM", "1:40PM", "1:50PM",
                "2:00PM", "2:10PM", "2:20PM", "2:30PM", "2:40PM", "2:50PM"]
    return render_template('chart.html', values=temperatures[-10:], labels=times[-10:], legend=legend)        


@landing.route('/hub/{<string:meth>}')
    
@landing.route('/hub', methods=['GET'])
@landing.route('/hub/<string:meth>', methods=['GET'])
def hub(meth="none"):
    
    # Get data from database
    if (meth.lower() == "lora"):
        futair_data = json.load(open(LORA_DB))
    
    elif (meth.lower() == "mqtt"):
        futair_data = json.load(open(MQTT_DB))
    else:
        futair_data = json.load(open(FAKE_DB))
    #try:
    #    # Get data from database
    #    if (meth.lower() == "lora"):
    #        futair_data = json.load(open(LORA_DB))
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
