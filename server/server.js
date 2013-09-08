var express = require('express'),
foos = require('./routes/places');
 
var app = express();
 
app.get('/places', foos.findAll);
app.get('/places/:id', foos.findById);
 
app.listen(3000);
console.log('Listening on port 3000...');
