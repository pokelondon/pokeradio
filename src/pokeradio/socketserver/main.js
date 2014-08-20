var PORT = 8001;
var REDIS = { host: 'localhost', port: 6379 };

var redis = require('socket.io-redis');
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

var nsp_app = io.of('/app');
var nsp_player = io.of('/player');

io.adapter(redis(REDIS));

var users = {};


nsp_app.on('connection', function(socket){
    var addedUser = false;
    var interv = null;
    var percent = 0;

    console.log('Connected to app');
    socket.emit('connected', 'connected to app');

    socket.on('add user', function (username) {
        // we store the username in the socket session for this client
        socket.username = username;
        // add the client's username to the global list
        users[username] = username;
        addedUser = true;

        // echo globally (all clients) that a person has connected
        socket.broadcast.emit('user joined', {
            username: socket.username
        });
    });

    socket.on('disconnect', function() {
        console.log('user disconnected', socket.username);

        if(addedUser) {
            delete users[socket.username];
        }

        clearInterval(interv);
    });

    interv = setInterval(function() {
        if(percent >= 100) {
            percent = 0;
        }
        percent ++;
        nsp_app.emit('play:progress', JSON.stringify({'playback_state': 'playing', 'track_length': 500, 'percentage': percent }).toString());
    }, 5000);
});

http.listen(PORT, function(){
    console.log('Listening on *:' + PORT);
});

