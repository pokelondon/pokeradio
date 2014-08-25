var PORT = 8001;
var REDIS = { host: 'localhost', port: 6379 };

var redis = require('socket.io-redis');
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http, {transports: 'websocket'});

var nsp_app = io.of('/app');
var nsp_player = io.of('/player');

io.adapter(redis(REDIS));

var users = {};

io.use(function(socket, next) {
    console.log('Something happening', socket.request);
    next();
});

nsp_app.on('connection', function(socket){
    var addedUser = false;
    var interv = null;
    var percent = 0;

    console.log('Connected to app');
    socket.emit('connected', 'connected to app');

    socket.on('disconnect', function() {
        console.log('user disconnected');
        clearInterval(interv);
    });

    //interv = setInterval(function() {
        //if(percent >= 100) {
            //percent = 0;
        //}
        //percent ++;
        //nsp_app.emit('play:progress', JSON.stringify({'playback_state': 'playing', 'track_length': 500, 'percentage': percent }).toString());
    //}, 5000);
});

nsp_player.on('connection', function(socket){
    var interv = null;

    console.log('Connecte to player endpoint');

    socket.on('message', function(data) {
        console.log(data);
    });

    socket.on('hi', function(data) {
        console.log('HI EVENT');
    });

    socket.on('disconnect', function() {
        console.log('disconnected');
    });

    interv = setInterval(function() {
        console.log('sending message');
        nsp_app.emit('playlist:track_play', JSON.stringify({'track': '123'}));
    }, 5000);

});

http.listen(PORT, function(){
    console.log('Listening on *:' + PORT);
});

