var express = require('express');
var path = require('path');
var app = express();
var https = require('https');

// setup static files
app.use(express.static(path.join(__dirname, 'public')));



// setup forwarding to cloudant db
app.use('/sensors/:sensor/history', function(req, res) {

	console.log("Received req " + req.path);
  
  var sensorName = req.param('sensor');
  var days = req.param('days');
  // default history is 14 days, max history is 1 year
  if (isNaN(days) || days < 0 || days > 366) {
	days = 14;
  }
  var fromDate = new Date(new Date() - (86400000 * days)).toJSON();
  var toDate = new Date().toJSON();
  var params = '?startkey=[%22' + sensorName + '%22,%20%22' + fromDate + '%22]&endkey=[%22' + sensorName + '%22,%20%22' + toDate + '%22]' ;
  console.log('using params : ' + params);
  
  var cloudantOptions = {
	hostname: 'c0b33b28-0a38-42c3-af13-378cd52a76f1-bluemix.cloudant.com',
	port: 443,
	path: '/poseidonsensors/_design/sensors/_list/csv/history' + params,
	method: 'GET',
	auth: 'c0b33b28-0a38-42c3-af13-378cd52a76f1-bluemix:d2900df88463ca87fce86aaec41a77cdc49e0a085ccee8838adce7781d200471'
  };
 
  https.get(cloudantOptions, function(res1) {
	console.log("Got response: " + res1.statusCode);
	
	res1.on('data', function (chunk) {
		res.write(chunk);
	});
	res1.on('end', function (chunk) {
		res.end(chunk);
	});
	res1.on('error', function(e) {
	console.log("Got error: " + e.message);
	});
  });
    
});

// set default page
app.use('/' , function(req, res) {
	res.redirect('/sensors.html');
});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function(err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});


module.exports = app;
