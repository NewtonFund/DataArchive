var express = require('express');
var router = express.Router();
var path = require('path');
//var childProcess = require('child_process');
var fs = require('fs');
const { Pool } = require('pg');

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
  //console.log(req.body);
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

router.post('/query_full', function(req, res, next) 
{
  //console.log('are they printed? > < !');
  var query = req.body.queryModel,
      checkbox = req.body.checkboxModel;
  var RA = query.RA,
      DEC = query.DEC,
      RADIUS = query.RADIUS,
      MJD_min = query.MJD_min,
      MJD_max = query.MJD_max,
      EXPTIME_min = query.EXPTIME_min,
      EXPTIME_max = query.EXPTIME_max,
      AZI_min = query.AZI_min,
      AZI_max = query.AZI_max,
      ALT_min = query.ALT_min,
      ALT_max = query.ALT_max,
      SEEING_min = query.SEEING_min,
      SEEING_max = query.SEEING_max,
      AIRMASS_min = query.AIRMASS_min,
      AIRMASS_max = query.AIRMASS_max,
      TAGID = query.TAGID,
//      USERID = query.USERID,
      PROPID = query.PROPID,
      GROUPID = query.GROUPID,
      OBSID = query.OBSID,
      NLIMIT = query.LIMIT;

  var pos_condition = '',
      mjd_condition = '',
      exptime_condition = '',
      azimuth_condition = '',
      altitude_condition = '',
      seeing_condition = '',
      airmass_condition = '',
      tagid_condition = '',
//      userid_condition = '',
      propid_condition = '',
      groupid_condition = '',
      obsid_condition = '';

  // If query position
  if (checkbox.position) {
    pos_condition = '     scircle(spoint(RADIANS(' + RA + '), RADIANS(' + DEC + ')), RADIANS(' + RADIUS + '/60.))~coords ';
  };

  // If query mjd
  if (checkbox.mjd) {
    mjd_condition = ' AND mjd BETWEEN ' + MJD_min + ' AND ' + MJD_max + ' ';
  };

  // If query exposure time
  if (checkbox.exptime) {
    exptime_condition = ' AND exptime BETWEEN ' + EXPTIME_min + ' AND ' + EXPTIME_max + ' ';
  };

  // If query azimuth
  if (checkbox.azimuth) {
    azimuth_condition = ' AND azimuth BETWEEN ' + AZI_min + ' AND ' + AZI_max + ' ';
  };

  // If query altitude
  if (checkbox.altitude) {
    altitude_condition = ' AND altitude BETWEEN ' + ALT_min + ' AND ' + ALT_max + ' ';
  };

  // If query seeing
  if (checkbox.seeing) {
    seeing_condition = ' AND seeing BETWEEN ' + SEEING_min + ' AND ' + SEEING_max + ' ';
  };

  // If query airmass
  if (checkbox.airmass) {
    airmass_condition = ' AND \"AIRMASS\" BETWEEN ' + AIRMASS_min + ' AND ' + AIRMASS_max + ' ';
  };

  // If query tagid
  if (checkbox.tagid) {
    tagid_condition = ' AND \"TAGID_tsvector\" @@ to_tsquery(\'%' + TAGID + '%\') ';
  };

  // If query userid
//  if (checkbox.userid) {
//    userid_condition = ' AND \"USERID\" =\'' + USERID + '\' ';
//  };

  // If query propid
  if (checkbox.propid) {
    propid_condition = ' AND \"PROPID_tsvector\" @@ to_tsquery(\'%' + PROPID + '%\') ';
  };

  // If query groupgid
  if (checkbox.groupid) {
    groupid_condition = ' AND \"GROUPID\" =\'' + GROUPID + '\' ';
  };

  // If query obsid
  if (checkbox.obsid) {
    obsid_condition = ' AND \"OBSID\" =\'' + OBSID + '\' ';
  };

  var items = ' __obsnum, date, ra_degree, dec_degree, mjd, exptime, azimuth, altitude, \"AIRMASS\", seeing, \"TAGID\", \"PROPID\", \"GROUPID\", \"OBSID\" '

  var condition = pos_condition + mjd_condition + exptime_condition + azimuth_condition + altitude_condition + seeing_condition + airmass_condition + tagid_condition + propid_condition + groupid_condition + obsid_condition;

  condition = condition.slice(5,-1);
  
  var query_string = 'SELECT ' + items + ' FROM allkeys_testing_pgsphere_gin_matched_es WHERE ' + condition + ' LIMIT ' + NLIMIT

  console.log(query_string);

  pool.query(query_string, (err, result) => {
    if (err) {
      return console.error('Error executing query', err.stack)
    }
    //console.log(result);
    res.send(result);
    //res.render('table.ejs', { blabla: result });
  })

});


router.post('/get_files', function(req, res, next) 
{
  //console.log(req.body);
  var selected_rows = req.body;
  var query_string = 'SELECT __filename from allkeys WHERE __obsnum IN (' + selected_rows + ') ';
  
  pool.query(query_string, (err, result) => {
    if (err) {
      return console.log(err.stack)
    }
    var result_formatted = [];
    //console.log(result.rows.length);
    for (var i=0; i<result.rows.length; i++) {
      //console.log(result.rows[i].__filename);
      result_formatted.push(result.rows[i].__filename);
    }
    console.log(result_formatted);
    // Need full path here
    var filename = 'temp_files/fileList_' + Date.now() + '.txt';
    var filepath = path.join('/home/dbuser/DataArchive/pg-express-angularjs/public', filename);
    console.log(filename);

    fs.writeFileSync(filepath, result_formatted, function(err) {
      if(err) {
        return console.log(err);
      }
      else {
        console.log("File created.");
      }
    });

    // Only send back public path here
    res.send(filename);
    console.log(filename);
    
  })

});



router.post('/get_rows', function(req, res, next) 
{
  //console.log(req.body);
  var selected_rows = req.body;
  var query_string = 'SELECT * from allkeys WHERE __obsnum IN (' + selected_rows + ') ';
  
  pool.query(query_string, (err, result) => {
    if (err) {
      return console.log(err.stack)
    }

    // Only send back public path here
    res.send(result);
    //console.log(result);
    
  })

});


module.exports = router;

