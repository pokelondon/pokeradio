var env = process.argv.slice(2)[0];
var config = require('../config/' + env + '/socket');

var PORT = config.port;
var REDIS = { host: config.redis_host, port: config.redis_port, db: config.redis_db };

var redis = require('socket.io-redis');
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http, {transports: 'websocket'});

var nsp_app = io.of('/app');

io.adapter(redis(REDIS));

nsp_app.on('connection', function(socket){
    console.log('Connected to app');

    socket.on('disconnect', function() {
        console.log('User disconnected');
    });

});

http.listen(PORT, function(){
    console.log('Listening on *:' + PORT);
});
