var spawn = require('child_process').spawn;
//spawn('.\\node_modules\\.bin\\http-server.cmd');
spawn('.\\node_modules\\.bin\\twitter-proxy.cmd');
const express = require('express');
const bodyParser = require("body-parser");
const fs = require('fs');
const app = express();
const port = 8080;
const request = require('request');
const default_settings = {"from_year":2018,"from_month":1,"from_day":1,"from_hour":0,"from_minute":0, "to_year":2019,"to_month":12,"to_day":31,"to_hour":0,"to_minute":0,"number_tweets":30};
var settings_path = "./settings.json";
app.set("view engine", "ejs");
var path = require('path');
app.set("views", path.join(__dirname, "views"));
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());
app.use(express.static(__dirname + '/public'));
var dateFormat = require('dateformat');
const tweets = ['makeschool', 'newsycombinator', 'ycombinator'];

function get_results(tweet, settings, all_results, res)
{
    var date_from = new Date(parseInt(settings.from_year), parseInt(settings.from_month), parseInt(settings.from_day), parseInt(settings.from_hour), parseInt(settings.from_minute), 0, 0);
    var date_to = new Date(parseInt(settings.to_year), parseInt(settings.to_month), parseInt(settings.to_day), parseInt(settings.to_hour), parseInt(settings.to_minute), 0, 0);
    request('http://localhost:7890/1.1/statuses/user_timeline.json\?count\='+settings.number_tweets+'\&screen_name\='+tweet, function (error, response, body) {
        var results = new Object();
        results.tweet = tweet;
        results.items=new Array();
        if (!error && response.statusCode == 200) {
            json_items = JSON.parse(body);
            for (i = 0; i < json_items.length; i++) {
                var json_item = json_items[i];
                var item = {};
                created_at_parse = new Date(Date.parse(json_item['created_at']));
                if(created_at_parse < date_from || created_at_parse > date_to)
                {
                    continue;
                }
                created_at = dateFormat(json_item['created_at'], "yyyy-m-d h:MM:ss TT");
                url = json_item['entities']['urls'].length > 0 ? json_item['entities']['urls'][0]['url'] : "";
                text = json_item['text'];
                users = [];
                for(j=0; j<json_item['entities']['user_mentions'].length; j++)
                {
                    users.push(json_item['entities']['user_mentions'][j].screen_name);
                }
                
                item['Created At'] = created_at;
                item['Url'] = url;
                item['Content'] = text;
                item['Users'] = users.join(", ");
                results.items.push(item);
            } 
        }
        all_results.push(results);
        if(all_results.length == tweets.length)
        {
            res.render('index', {
                all_results: all_results,
                columns: ['Content','Created At','Url','User'],
                settings: settings
            });
         
        }
    });
}

function index_page(res)
{
    fs.readFile(settings_path, function (err, data) {
        
      var settigns = null;
      if (err) {
        settings =default_settings;
      }
      else
      {
          try
          {
               settings = JSON.parse(data.toString());
          }
          catch
          {
              settings =default_settings;
          }
      }

      var all_results = []
        
        for (i=0; i <tweets.length; i++) 
        {
            get_results(tweets[i], settings, all_results, res);
        }
    });
}

app.get('/', (req, res) => 
    {
        index_page(res);
    } 
);

app.post('/', (req, res) => 
    {
        fs.writeFile(settings_path, JSON.stringify(req.body), 'utf8', function(error) {  index_page(res);  });
    } 
);

app.listen(port);
console.log('Server running on http://localhost:8080');
console.log('Request the Twitter API using: http://localhost:7890/1.1/statuses/user_timeline.json\?count\=30\&screen_name\=makeschool');

