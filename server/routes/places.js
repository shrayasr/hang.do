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

exports.findById = function(req, res) {
  var id = req.params.id;
  console.log('Retrieving place: ' + id);
  db.collection('places', function(err, collection) {
    collection.findOne({'_id':new BSON.ObjectID(id)}, function(err, item) {
      res.send(item);
    });
  });
};

exports.addPlace = function(req,res) {
  var place = req.body;
  console.log('Adding place: ' + JSON.stringify(place));
  db.collection('places', function(err, collection) {
    collection.insert(place, {safe:true}, function(err, result) {
      if (err) {
        res.send({'error':'An error has occurred'});
      } else {
        console.log('Success: ' + JSON.stringify(result[0]));
        res.send(result[0]);
      }
    });
  });
};

