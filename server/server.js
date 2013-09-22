var express = require('express'),
    places = require('./routes/places'),
    home = require('./routes/home'),
    suggs = require('./routes/suggs');

var app = express();
app.use(express.bodyParser());

app.get('/', home.index);
app.get('/places/:id', places.findById);
app.get('/in/:place',suggs.get);
app.post('/places',places.addPlace);

app.listen(3000);
console.log('Listening on port 3000...');
