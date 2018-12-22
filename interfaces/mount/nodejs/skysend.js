var net = require('net');
var fs = require('fs');
var program = require('commander');

program
  .version('0.0.1')
  .description('Description:\n\n    sends contents of a JavaScript file to TheSkyX on a remote machine')
  .usage('<address> <file>')
  .arguments('<address> <file>')
  .action(function (address, file) {
    addressValue = address;
    fileValue = file;
  });

program.parse(process.argv);

if (typeof addressValue === 'undefined') {
  console.error('no address given !');
  process.exit(1);
}

var client = new net.Socket();

client.setEncoding('utf8');

client.connect(3040, addressValue, function() {
  // console.log('Connected');
  var data = fs.readFileSync(fileValue, { encoding: 'utf8' });
  client.write(data);
});

client.on('data', function(data) {
  console.log(data.trim());
  client.destroy(); // kill client after server's response
});

client.on('error', function(err) {
  console.log('Error: ' + err.message);
  client.destroy(); // kill client after server's response
});

client.on('close', function() {
  // console.log('Connection closed');
});