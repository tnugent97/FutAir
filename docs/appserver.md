Step-by-step build your own application server

This guide will take you through setting up a LoRaWAN™ application server to communicate with devices connected to the Things Connected test bed. To receive PUSH notifications the application server should implement the methods defined in the Everynet Core API.


Prerequisites


1. Access to Things Connected testbed

2. Register a device

3. Have a machine/server (with a public IP address) to run Node.js on


Setup


4. Download and install Node.js

5. Create a new Node.js project and install the modules needed by the application server:


cd $HOME

mkdir app

cd app

npm init


Just press return to accept the default answer to any question asked.


sudo npm install jayson atob cors connect body-parser btoa


Implement the application server


6. Create the main script and open it in your favourite editor:


vim index.js


7. Require the modules needed:


const jayson = require('jayson');

const atob = require('atob');

const cors = require('cors');

const jsonParser = require('body-parser').json;

const btoa = require('btoa');

const fs = require('fs');

const connect = require('connect');

const app = connect();


8. Define a log file where to store messages received from the Everynet Network.


var date = new Date().toISOString().replace(/T/, '_').replace(/-/g, '').replace(/:/g, '').replace( /\..+/, '');

var filepath = './log_data_' + date;


9. Create the server, implement the uplink and downlink methods according to the Everynet Core API, start the server on port 9090:


var server = jayson.server({

uplink: function(args, callback) {

/* Print out the uplink message received from the Everynet Network on the console and

* append it to the log file.

*/

console.log("Received uplink: " + JSON.stringify(args, null, 4) + "\n");

fs.appendFile(filepath, "Received uplink: " + JSON.stringify(args, null, 4) + "\n");

/* Get the payload (base64 encoded), which includes actual data sent by the device,

* convert it to ASCII format, print it out on the console and append it to the log file.

* We assume the device is sending a string.

*/

var buffer = new Buffer(args.payload, 'base64');

console.log("Payload: " + buffer.toString('ascii') + "\n");

fs.appendFile(filepath, "Payload: " + buffer.toString('ascii') + "\n");


callback(null, "200");

},

downlink: function(args, callback) {


/* Print out the downlink message received from the Everynet Network on the console and

* send back an ACK, which will then be sent to the device.

*/

console.log("Received downlink: " + JSON.stringify(args, null, 4));

var reply = {

payload: btoa("ACK")

};

callback(null, reply);

}

});


app.use(cors({methods: ['POST', 'GET']}));

app.use(jsonParser());

app.use(server.middleware());

app.listen(9090);


10. Run the server:


node index.js


Now assume our device is sending a 6-byte payload having the following format:


In the uplink method, we need to parse the payload as in the following:


uplink: function(args, callback) {

/* Print out the uplink message received from the Everynet Network on the console and

* append it to the log file.

*/

console.log("Received uplink: " + JSON.stringify(args, null, 4) + "\n");

fs.appendFile(filepath, "Received uplink: " + JSON.stringify(args, null, 4) + "\n");

/* Get the payload (base64 encoded), which includes actual data sent by the device,

* convert it to hex format.

*/

var buffer = new Buffer(args.payload, 'base64');

var hex = buffer.toString(‘hex’);

/* Parse the payload, print it on the console, and append it to the log file */

var temp = parseInt(hex[2].concat(hex[3]), 16);

if (temp > 0x7F)

temp = temp - 1 - 0xFF; // Signed, in two’s complement

var u_count = parseInt(hex[4].concat(hex[5]), 16);

var d_count = parseInt(hex[6].concat(hex[7]), 16);

var voltage = parseInt(hex[8].concat(hex[9]).concat(hex[10]).concat(hex[11]), 16);

var payload = {Temperature: temp, Uplink_counter: u_count, Downlink_counter: d_count, Battery_voltage: voltage};

console.log("Payload: " + JSON.stringify(payload, null, 4));

fs.appendFile(filepath, "Payload: " + JSON.stringify(payload, null, 4) + "\n");


callback(null, "200");

},
