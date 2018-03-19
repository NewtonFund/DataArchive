var express = require('express');
var router = express.Router();
var path = require('path');
const { Pool } = require('pg')

const pool = new Pool({
  user: 'dbuser',
  host: '150.204.240.113',
  database: 'ltarchive',
  password: 'dbuser',
  port: 6543,
})

/* GET home page. */
router.get('/', function(req, res, next) 
{
  //req.body.username
  //res.render('index', { title: 'Express' });
  //res.send("Hello");
  res.sendFile(path.join(__dirname, '../', 'index.html'));
    
});

router.get('/query_fixed', function(req, res, next) 
{

  pool.query('SELECT __obsnum, __filename, Date, ra_degree, dec_degree from allkeys limit 10', (err, result) => {
    if (err) {
      return console.error('Error executing query', err.stack)
    }
    //console.log('hello');
    res.send(result);
    //res.render('table.ejs', { blabla: result });
  })

});

router.post('/query_obsnum', function(req, res, next) 
{
  console.log(req.body);
  var min = req.body.minval;
  pool.query('SELECT __obsnum, __filename, Date, ra_degree, dec_degree from allkeys WHERE __obsnum > ' + min + ' limit 10', (err, result) => {
    if (err) {
      return console.error('Error executing query', err.stack)
    }
    //console.log(result);
    res.send(result);
    //res.render('table.ejs', { blabla: result });
  })

});

module.exports = router;
