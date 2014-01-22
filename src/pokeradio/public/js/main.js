require.config({
    paths: {
        jquery: '//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min',
        backbone: 'lib/backbone/backbone.min',
        underscore: 'lib/underscore/underscore',
        iobind: 'lib/backbone/backbone.iobind.min',
        iosync: 'lib/backbone/backbone.iosync.min',
        bootstrap: 'lib/bootstrap/bootstrap'
    },
    shim:{
        'backbone': {
            deps: ['underscore','jquery'],
            exports: 'Backbone'
        },
        'underscore': {
            deps: ['jquery'],
            exports: '_'
        },
        'bootstrap': {
            deps: ['jquery'],
            exports: '$'
        },
        'iosync': {
            deps: ['jquery', 'underscore', 'backbone'],
            exports: 'iosync'
        },
        'iobind': {
            deps: ['jquery', 'underscore', 'backbone', 'iosync'],
            exports: 'iobind'
        }
    }
});

define(['app'],function(app){
    app.init();
    });
