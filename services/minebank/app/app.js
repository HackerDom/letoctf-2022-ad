const express = require("express");
const cookieParser = require("cookie-parser");
const bodyParser = require('body-parser');

const app = express();

app.use(function (err, req, res, next) {
    console.log(err.stack)
    res.status(500).send('')
    //next(err)
});

const db = require("./models");
// TODO: turn off force or delete this param
db.sequelize.sync({ force: true }); // for production use without args
app.use(function (req, resp, next) {
    req.db = db;
    next();
})

app.use('/static', express.static(__dirname + '/views/static'));

app.use(cookieParser());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.raw({
    inflate: true,
    limit: '100kb',
    type: 'application/xml'
}));

app.use(require("./api"))

app.listen(1337, function() {
    console.log(`[+] Service started on 1337 port`)
});