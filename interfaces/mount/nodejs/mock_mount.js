#!/usr/bin/env node

var program = require('commander');

program
  .version('0.0.1')
  .description('Description:\n\n    doesn\'t send a mount command to TheSkyX')
  .option('-v, --verbose', 'Verbosity')
  .usage('command [arguments]');

program
  .command('position')
  .description('gets telescope position')
  .action(function(options) {
    console.log("RA: 10h 12m 56.3s|Dec: +37° 35' 13.0\"|Alt: -4.15|Az: 3.14|HA: 4.24|Track: 1");
  });

program
  .command('goto <name>')
  .description('telescope slews to target location')
  .action(function(name, options) {
      console.log("Slew complete.");
  });

program
  .command('dither <arcmin> <direction>')
  .description('telescope dithers around location')
  .action(function(arcmin, direction, options) {
    console.log("Dither complete.");
  });

program
  .command('radec <ra> <dec>')
  .description('slews telescope to RA and DEC using strings')
  .action(function(ra, dec, options) {
    console.log("Slew to RA/Dec complete.");
  });

program
  .command('decimal <ra> <dec>')
  .description('slews telescope to RA and DEC using decimal numbers')
  .action(function(ra, dec, options) {
    console.log("Slew to RA/Dec complete.");
  });

program
  .command('altaz <alt> <az>')
  .description('slews telescope to ALT and AZ')
  .action(function(alt, az, options) {
    console.log("Slew to Alt-Az complete.");
  });

program
  .command('take <time>')
  .description('take an image with ccd using exposure time')
  .action(function(time, options) {
      console.log("Image taken|Location: /Users/SohrabZ/Desktop/fits/test.fits");
  });

program
  .command('home')
  .description('slews telescope to home position')
  .action(function(options) {
    console.log("Mount homed. LastSlewError: 0");
  });

program
  .command('park')
  .description('slews telescope to park position')
  .action(function(options) {
    console.log("Mount parked. LastSlewError: 0");
  });

program
  .command('purge')
  .description('purges the serial port')
  .action(function(options) {
    console.log("Serial port purged");
  });

program
  .command('start')
  .description('starts telescope tracking')
  .action(function(options) {
    console.log("Mount tracking off. LastSlewError: 0|Track: 1");
  });

program
  .command('stop')
  .description('stops telescope tracking')
  .action(function(options) {
    console.log("Mount tracking off. LastSlewError: 0|Track: 0");
  });

program
    .command('radec2altaz')
    .description('converts ra, dec to alt, az')
    .action(function(options) {
        console.log("Alt: 45.2315|Az: 12.5643");
    });

program.parse(process.argv);

process.exit(1);
