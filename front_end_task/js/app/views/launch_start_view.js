// Conversion of CommonJS modul to work with RequireJS (example: node r.js -convert path/to/commonjs/modules/ path/to/output)
define(function (require, exports, module) {
    //CommonJS modul content
    var Backbone            = require('backbone');
    var  launch_start = Backbone.View.extend({
        initialize: function(args) {
            _.bindAll(this, 'status');
            this.model.bind('change:status', this.status);
        },
        el : document.getElementById('launch_start'),
        events : {
            "change" : "refresh"  
        },
        refresh : function() {              
            this.model.set({"status" : "refresh"});
        },
        status: function() {
            var state = this.model.get('status');
            if(state == "cancel")
            {
                this.el.checked = this.model.localStorage["launch_start"];
            }
            else if(state=="ok")
            {
                this.model.localStorage["launch_start"] = this.el.checked; 
            }
        },
    });

    module.exports = launch_start;
});
