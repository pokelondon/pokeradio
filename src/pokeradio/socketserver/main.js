var PORT = 8001;
var SOCKET = 'unix:/tmp/poke_pokeradio_sockets_live.sock';
var REDIS = { host: 'localhost', port: 6379 };

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

