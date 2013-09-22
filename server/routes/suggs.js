var mongo = require('mongodb');

var Server = mongo.Server,
    Db = mongo.Db,
    BSON = mongo.BSONPure;

var server = new Server('localhost', 27017, {auto_reconnect: true});
db = new Db('placesdb', server,{w:1});

db.open(function(err, db) {
  if(!err) {
    console.log("Connected to db");
    db.collection('places', {strict:true}, function(err, collection) {
      if (err) {
        console.log("the collection places doesn't exist");
        db.createCollection("places",{},function(){
          console.log('collection created');
        });
      }
    });
  }
});

exports.get = function(req, res) {
  var place = req.params.place.toLowerCase();
  
  console.log('Retrieving suggestion around : ' + place);
  var data = {};
  
  var coll = db.collection('places');
  var val = coll.find({'$and':[{location_specific:place},{type:'movie'}]},{sort:{rating:-1}}).toArray(function(err, item) {
    var data = {};
    data.movie = item;
    var val = coll.find({'$and':[{location_specific:place},{type:'movie'}]},{sort:{rating:-1}}).toArray(function(err, item) {
      data.rest = item;
      var send = [];
      for(var i= 0; i<data.movie.length;i++){
        var hang = {};
        send.push({movie: data.movie[i], rest:data.rest[i]});
      }
      res.send(send);
    });
  });
};

