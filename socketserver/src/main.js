var PORT = (process.env.PORT || 8080);

var redisAdapter = require('socket.io-redis');
var redis = require('redis')
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http, {transports: 'websocket'});

var nsp_app = io.of('/app');

var REDIS_HOST = process.env.REDIS_PORT_6379_TCP_ADDR || 'redis';
var REDIS_PORT = process.env.REDIS_PORT_6379_TCP_PORT || 6379;

var pub = redis.createClient(REDIS_PORT, REDIS_HOST);
var sub = redis.createClient(REDIS_PORT, REDIS_HOST);

io.adapter(redisAdapter({pubClient: pub, subClient: sub}));

var connections = 0;

nsp_app.on('connection', function(socket){
    connections ++;
    console.log('Connected to app', connections);

    socket.on('disconnect', function() {
        connections --;
        console.log('User disconnected', connections);
    });

});

http.listen(PORT, function(){
    console.log('Listening on *:' + PORT);
});
