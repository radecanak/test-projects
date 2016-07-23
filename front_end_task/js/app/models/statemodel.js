// Conversion of CommonJS modul to work with RequireJS (example: node r.js -convert path/to/commonjs/modules/ path/to/output)
define(function (require, exports, module) {
    //CommonJS modul content
    var Backbone            = require('backbone');
    var state_model = Backbone.Model.extend({
        initialize: function () {
            //storage of Launch on PC start and  Launch minimized in system tray states
            this.localStorage = {};
            this.localStorage["launch_minimized"] = false;
            this.localStorage["launch_start"] = false;
        }
        
    });
    
    module.exports = state_model;
});