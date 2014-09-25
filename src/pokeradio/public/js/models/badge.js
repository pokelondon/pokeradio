/**
 * Badge Model
 */

define(
    [   'jquery',
        'backbone',
        'underscore'
    ],
    function($, Backbone, _) {
        var Model = Backbone.Model.extend({
            defaults: {
                type: 'info'
            }
        });
        return Model;
    }
);
