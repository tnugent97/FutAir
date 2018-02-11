const jayson = require('jayson');

const atob = require('atob');

const cors = require('cors');

const jsonParser = require('body-parser').json;

const btoa = require('btoa');

const fs = require('fs');

const connect = require('connect');

const app = connect();



var date = new Date().toISOString().replace(/T/, '_').replace(/-/g, '').replace(/:/g, '').replace( /\..+/, '');

var filepath = './log_data_' + date;



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