# Embedded

## Capabilities
* Complete power management system for running off battery, and charging the battery using our solar panel.
* Deepsleep implemented so that power consumption can be kept low, and readings taken every 30 minutes.
* Pressure sensor, temperature and humidity sensor and custom PCB made for NO2 and CO sensor.
* MQTT implemented on ESP, sending data across EERover to paho.
* Government IoT trial LORA WAN implemented on server-side (govt run), client-side (running on raspberry pi) and on an M0 with radio antenna.
* Data successfully received from MQTT and LORA network and linked to the website so graphs and map are automatically updated with new data.
* 3D printed case including foldout for maximum solar surface area, render on website from CAD software.
* LCD monitor set up and running - but not enough memory to run all of the above.

## Running the website
The website and all of its code is contained in the [website](website). The [README](website/README.md) in that directory contains instructions how to run the website (requires Python and pip).

Basic setup is `pip install -r requirements.txt` and `python2 main.py` in the website directory.

### lora_app

This folder contains client-side server code for interfacing with our application on the LORA network.

## lora

This folder has the code that runs on the M0 for connecting to the LORA WAN network, and screengrabs demonstrating our testing of sending data from the device to the BT tower using the LORA network, and then forwarding the data using the API to our server running on a raspberry pi.

## src

This folder contains all of the code that runs on the ESP for the various sensors.

## Renders

Contains renders of our 3D model for 

## Running files on the ESP

Using screen, you can run a files like so:

`exec(open("./src/main.py").read())`

`exec(open("read.py").read())`

`exec(open("temp_hum_read.py").read())`

`exec(open('mqtt_sensors.py').read())`
