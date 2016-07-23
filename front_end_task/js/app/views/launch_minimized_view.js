// Conversion of CommonJS modul to work with RequireJS (example: node r.js -convert path/to/commonjs/modules/ path/to/output)
define(function (require, exports, module) {
    //CommonJS modul content
    var Backbone            = require('backbone');
    var launch_minimized = Backbone.View.extend({
        initialize: function(args) {
            _.bindAll(this, 'status');
            this.model.bind('change:status', this.status);
        },
        status: function() {
            var state = this.model.get('status');
            if(state == "cancel")
            {
                this.el.checked = this.model.localStorage["launch_minimized"];
            }
            else if(state == "ok")
            {
                this.model.localStorage["launch_minimized"] = this.el.checked; 
            }
        },
        el : document.getElementById('launch_minimized'),
        events : {
            "change" : "refresh"  
        },
        refresh : function() {              
            this.model.set({"status" : "refresh"});
        }
    });

    module.exports = launch_minimized;
});