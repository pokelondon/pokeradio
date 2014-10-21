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

var connections = 0;

nsp_app.on('connection', function(socket){
    connections ++;
    console.log('Connected to app', connections);

    var interval2;
    //var ids = [
        //18971, 18975, 18976, 18977, 18978, 18981, 18980, 18979, 18982, 18983, 18984
    //];

    //var interval2 = setInterval(function() {
        //var id = ids.shift();
        //if (!id) {
            //clearInterval(interval2);
            //console.log('Done');
        //}
        //var data = {
            //"id": id,
        //};
        //console.log('played', id);
        //socket.emit('playlist:played', JSON.stringify(data));
    //}, 10000);


    socket.on('disconnect', function() {
        connections --;
        console.log('User disconnected', connections);
        clearInterval(interval2);
    });

});

http.listen(PORT, function(){
    console.log('Listening on *:' + PORT);
});
