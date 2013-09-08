var express = require('express'),
places = require('./routes/places');
 
var app = express();
app.use(express.bodyParser());

app.get('/places', places.findAll);
app.get('/places/:id', places.findById);
app.post('/places',places.addPlace);
 
app.listen(3000);
console.log('Listening on port 3000...');
