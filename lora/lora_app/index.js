const jayson = require('jayson');
const atob = require('atob');
const cors = require('cors');
const jsonParser = require('body-parser').json;
const btoa = require('btoa');
const fs = require('fs');
const connect = require('connect');
const app = connect();
//var http = require('http');
var date = new Date().toISOString().replace(/T/, '_').replace(/-/g, '').replace(/:/g, '').replace( /\..+/, '');
var filepath = './log_data_' + date;

var server = jayson.server({
    uplink: function(args,callback){
         /* Print out the uplink message received from the lora network on the console and
        * append it to the log file.
        */
        console.log("Received uplink: " + JSON.stringify(args,null,4) + "\n");
        fs.appendFile(filepath, "Received uplink: " + JSON.stringify(args,null,4) + "\n");
        /* Get the payload (base 64) which includes the actual data
        * convert the data ASCII and print it out. */
        var buffer = new buffer(args.payload, 'base64');
        console.log("Payload: " + buffer.toString('ascii') + "\n");
        fs.appendFile(filepath, "Payload: " + buffer.toString('ascii') + "\n");

        callback(null,"200");
    },
    downlink: function(args,callback){
        /*
        Print the downlink message received from the network on the console,
        Send back an ACK which will then be sent to the device
        */
        console.log("Received downlink: " + JSON.stringify(args, null, 4));
        var reply = {
            payload: btoa("ACK")
        };
        callback(null, reply);
    }
});
/*
http.createServer(function (req, res) {
	res.writeHead(200, {'Content-Type': 'text/plain'});
	res.end('Hello World!');
}).listen(9090);
*/
app.use(cors({methods: ['POST', 'GET']}));

app.use(jsonParser());

app.use(server.middleware());

app.listen(9090);
