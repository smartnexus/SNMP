const express = require('express');
const request = require('request');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();

app.use(express.json());
app.use(bodyParser.urlencoded({extended: false}));

const addressDetails = JSON.parse(fs.readFileSync('address.json'));

const remote = JSON.parse(fs.readFileSync('ips.json'));

app.post('/slack/actions', function (req, res) {
	console.log('[ROUTING APP]: Received http POST from slack, routing to endpoints...');
	var info = req.body.payload;
	for (var i = 0; i < remote.length; i++) {
		var ip = remote[i];
		request.post('http://' + ip + ':5000/slack/actions', {
		  form: {
		    payload: info
		  }
		}, function (err, httpResponse, body) {
			if(!err) {
				console.log('[' + ip + ']: Received httpStatus code ' + httpResponse.statusCode);
			}
		})	
	}
	res.sendStatus(200);
});

app.listen(addressDetails.port, addressDetails.ip, function () {
	console.log('[ROUTING APP]: Read %s ips from database: [%s]', remote.length, remote);
	console.log('[ROUTING APP]: Starting server on %s:%s', addressDetails.ip, addressDetails.port);
});
