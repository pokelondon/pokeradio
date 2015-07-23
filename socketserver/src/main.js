var PORT = (process.env.PORT || 8080);

var sio_redis = require('socket.io-redis');
var redis = require('redis')
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http, {transports: 'websocket'});

var nsp_app = io.of('/app');

var REDIS_HOST = process.env.REDIS_PORT_6379_TCP_ADDR || 'redis';
var REDIS_PORT = parseInt(process.env.REDIS_PORT_6379_TCP_PORT, 10) || 6379;

var pub = redis.createClient(REDIS_PORT, REDIS_HOST, {return_buffers: true});
var sub = redis.createClient(REDIS_PORT, REDIS_HOST, {return_buffers: true});
var redis_client = redis.createClient(REDIS_PORT, REDIS_HOST, {return_buffers: true});

io.adapter(sio_redis({pubClient: pub, subClient: sub}));

var connections = 0;
var playback_state = '';

nsp_app.on('connection', function(socket){
    connections ++;
    console.log('Connected to app', connections);

    socket.on('disconnect', function() {
        connections --;
        console.log('User disconnected', connections);
    });
});

app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    res.setHeader("Content-type", 'application/json');
    next();
});

app.get('/connections', function(req, res) {
    redis_client.get('playback_state', function(err, reply) {
        playback_state = reply;
        if(err) {
            res.json({'connections': connections, 'playback_state': ''});
        } else {
            res.json({'connections': connections, 'playback_state': playback_state});
        }
    });
});

http.listen(PORT, function(){
    console.log('Listening on *:' + PORT);
});
