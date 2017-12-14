// RJS 2017-12-14
// Testing the statement that asynchronous IO in node.js does not 
// block multiple connections to the server.
//
// You need a large text file on disk called datafile.txt.
// I just used a random syslog.
//
// Run this code in a console with the command "node simul.js".
// Then connect from multiple browsers at the same time to http://127.0.0.1:3030/
// Easier might be just to run
//   curl "http://127.0.0.1:3030/"
// in multiple shells
//
// All connections should be able to read the file and stream back the
// response simultaneously.

const http = require('http');
const hostname = '127.0.0.1';
const port = 3030;

const server = http.createServer((request, response) => {

  var fs = require('fs');

  response.statusCode = 200;
  response.setHeader('Content-Type', 'text/plain');

  fs.readFile('datafile.txt', 'utf8', function(err, contents) {
    response.write(contents);
    response.end('End of datafile.txt\n');
  });
  
  console.log(`Printing this to the console at same time as reading the file.`);

});

server.listen(port, hostname, () => {
});

