# FutAir

## Capabilities
* Complete power management system for running off battery, and charging the battery using our solar panel.
* Deepsleep implemented so that power consumption can be kept low, and readings taken every 30 minutes.
* Pressure sensor, temperature and humidity sensor and custom PCB made for NO2 and CO sensor.
* MQTT implemented on ESP, sending data across EERover to paho.
* Government IoT trial LORAWAN implemented on server-side (https://www.thingsconnected.net/), client-side (running on raspberry pi) and on a cortex-m0 with 868MHz radio antenna. (BT tower was the tested GateWay).
* Data successfully received from MQTT and LORA network and linked to the website so graphs and map are automatically updated with new data.
* 3D printed case including foldout for maximum solar surface area, render on website from CAD software.
* LCD monitor set up and running - but not enough memory to run all of the above.
* Schematic for PCB for the full product with cortex-M0, RFM95, Si7021, BMP180, MiCS-4514, ADS1115 with power and serial interface has been designed, alas abandoned due to PCB lead times.
* Colour sensor code which was not required.

## Running the website
The website and all of its code is contained in the [website](website). The [README](website/README.md) in that directory contains instructions how to run the website (requires Python and pip).

Basic setup is `pip install -r pip_requirements.txt` and `python2 main.py` in the website directory. (`python3 main.py`) should also work.

index.html is the main home page of the website where information on the product can be found along with marketing information.

hub.html is a map view of London showing what a network of FutAirs would look like. Id-1 is our real life sensors and all the others are randomly generated.

chart.html is the page for viewing the graphs of data from the various sensors on a device. These charts can be vied by clicking on the ID from the hub.html page.

### lora_app

This folder contains client-side node.js server code for interfacing with our application on the LORAWAN network. 

## lora

This folder has the code that runs on the cortex-m0 for connecting to the LORAWAN network, and screengrabs demonstrating our testing of sending data from the device to the BT tower using the LORA network, and then forwarding the data using the API to our server running on a raspberry pi.

## src

This folder contains all of the code that runs on the ESP for the various sensors. The directory `src/combined/` contains the full project, with all required python files. Other directories in `src` contain the individual modules with tests.

## Renders

Contains renders of our 3D model for case with solar panel.

## Running files on the ESP

Using screen, you can run a files like so:

`exec(open("file.py").read())`

