#!/usr/bin/env node

var program = require('commander');
var execSync = require('child_process').execSync;
var exec = require('child_process').exec;
var sleep = require('sleep');
var multiline = require('multiline');
var fs = require('fs');
var javascript = "";

program
  .version('0.0.2')
  .description('Description:\n\n    sends a mount command to TheSkyX')
  .option('-v, --verbose', 'Verbosity')
  .usage('command [arguments]');

program
  .command('position')
  .description('gets telescope position')
  .action(function(options) {
    javascript = multiline(function() {/* 
      var Out;
      var dRA;
      var dDec;
      var dAz;
      var dAlt;
      var coordsString1;
      var coordsString2;
      sky6RASCOMTele.Connect();
      if (sky6RASCOMTele.IsConnected == 0) {
        Out = "Not connected"
      } else {
        sky6RASCOMTele.GetRaDec();
        dRA = sky6RASCOMTele.dRa;
        dDec = sky6RASCOMTele.dDec;
        sky6Utils.ComputeHourAngle(dRA);
        dHA = sky6Utils.dOut0;
        sky6Utils.ConvertEquatorialToString(dRA, dDec, 5);
        coordsString1 = sky6Utils.strOut;
        sky6RASCOMTele.GetAzAlt();
        Out = coordsString1.trim().replace("  Dec", "|Dec");
        Out += "|Alt: " + parseFloat(Math.round(sky6RASCOMTele.dAlt*100)/100).toFixed(2);
        Out += "|Az: " + parseFloat(Math.round(sky6RASCOMTele.dAz*100)/100).toFixed(2);
        Out += "|HA: " + parseFloat(Math.round(dHA*10000)/10000).toFixed(4);
        Out += "|Track: " + sky6RASCOMTele.IsTracking;
      };
    */});
    javascript = "/* Java Script */\n" + javascript;
  });

program
  .command('radec2altaz <radec>')
  .description('converts ra, dec to alt, az')
  .action(function(radec, options) {
    javascript = multiline(function() {/*
      var radec = "$radec";
      var ra = parseFloat(radec.split(",")[0]);
      var dec = parseFloat(radec.split(",")[1]);
      sky6Utils.ConvertRADecToAzAlt(ra, dec);
      "Alt: " + sky6Utils.dOut1 + "|Az: " + sky6Utils.dOut0;
    */});
    javascript = javascript.replace('$radec', radec);
    javascript = "/* Java Script */\n" + javascript;
  });

program
  .command('goto <name>')
  .description('telescope slews to target location')
  .action(function(name, options) {
    javascript = multiline(function() {/* 
      var Target = "%s";
      var TargetRA = 0;
      var TargetDec = 0;
      var Out = "";
      var err;
      sky6StarChart.LASTCOMERROR = 0;
      sky6StarChart.Find(Target);
      err = sky6StarChart.LASTCOMERROR;
      if (err != 0) {
        Out =Target + " not found.";
      } else {
        sky6ObjectInformation.Property(54); 
        TargetRA = sky6ObjectInformation.ObjInfoPropOut;
        sky6ObjectInformation.Property(55);
        TargetDec = sky6ObjectInformation.ObjInfoPropOut;
        Out = String(TargetRA) + "|"+ String(TargetDec);
        sky6RASCOMTele.Connect();
        if (sky6RASCOMTele.IsConnected == 0) {
          Out = "Not connected";
        } else {
          sky6RASCOMTele.Asynchronous = 0;
          sky6RASCOMTele.Abort();
          sky6RASCOMTele.SlewToRaDec(TargetRA, TargetDec, "");
          while(!sky6RASCOMTele.IsSlewComplete) {
            sky6Web.Sleep(1000);
          }
          Out = "Slew complete.";
        }
      }
    */});
    javascript = javascript.replace('%s', name);
    javascript = "/* Java Script */\n" + javascript;
  });

program
  .command('dither <arcmin> <direction>')
  .description('telescope dithers around location')
  .action(function(arcmin, direction, options) {
    direction = direction.charAt(0).toUpperCase();
    if(direction != 'N' && direction != 'S' && direction != 'E' && direction != 'W' && direction != 'U' && direction != 'D' && direction != 'L' && direction != 'R') {
      process.exit(1);
    } else {
      new_direction = "'" + direction + "'";
      // console.log('Dithered %s arc minutes %s around target', arcmin, direction);
      javascript = multiline(function() {/* 
        var Out = "";
        sky6RASCOMTele.Connect();
        if (sky6RASCOMTele.IsConnected == 0) {
          Out = "Not connected";
        } else {
          sky6RASCOMTele.Asynchronous = 0;
          sky6RASCOMTele.Abort();
          sky6RASCOMTele.Jog($arcmin, $direction);
          while(!sky6RASCOMTele.IsSlewComplete) {
            sky6Web.Sleep(1000);
          }
          Out = "Dither complete.";
        }
      */});
      javascript = javascript.replace('$arcmin', arcmin);
      javascript = javascript.replace('$direction', new_direction);
      javascript = "/* Java Script */\n" + javascript;
    }
  });

program
  .command('radec <ra> <dec>')
  .description('slews telescope to RA and DEC using strings')
  .action(function(ra, dec, options) {
    // console.log(ra + " " + dec);
    javascript = multiline(function() {/* 
      var Out = "";
      var dRA = 0.0;
      var dDec = 0.0;
      sky6RASCOMTele.Connect();
      if (sky6RASCOMTele.IsConnected == 0) {
        Out = "Not connected";
      } else {
        sky6Utils.ConvertStringToRA("$ra");
        dRA = sky6Utils.dOut0;
        Out = dRA;
        sky6Utils.ConvertStringToDec("$dec");
        dDec = sky6Utils.dOut0;
        Out += " " + dDec;
        sky6RASCOMTele.Asynchronous = 0;
        sky6RASCOMTele.Abort();
        sky6RASCOMTele.SlewToRaDec(dRA, dDec, 'radec_coords');
        while(!sky6RASCOMTele.IsSlewComplete) {
          sky6Web.Sleep(1000);
        }
        Out = "Slew to RA/Dec complete.";
      }
    */});
    javascript = javascript.replace('$ra', ra);
    javascript = javascript.replace('$dec', dec);
    javascript = "/* Java Script */\n" + javascript;
  });

program
  .command('decimal <radec>')
  .description('slews telescope to RA and DEC using decimal numbers')
  .action(function(radec, options) {
    javascript = multiline(function() {/* 
      var Out = "";
      var radec = "$radec";
      var dRA = parseFloat(radec.split(',')[0]);
      var dDec = parseFloat(radec.split(',')[1]);
      sky6RASCOMTele.Connect();
      if (sky6RASCOMTele.IsConnected == 0) {
        Out = "Not connected";
      } else {
        Out = dRA;
        Out += " " + dDec;
        sky6RASCOMTele.Asynchronous = 0;
        sky6RASCOMTele.Abort();
        sky6RASCOMTele.SlewToRaDec(dRA, dDec, 'radec_coords');
        while(!sky6RASCOMTele.IsSlewComplete) {
          sky6Web.Sleep(1000);
        }
        Out = "Slew to RA/Dec complete.";
      }
    */});
    javascript = javascript.replace('$radec', radec);
    javascript = "/* Java Script */\n" + javascript;
  });

program
  .command('altaz <alt> <az>')
  .description('slews telescope to ALT and AZ')
  .action(function(alt, az, options) {
    javascript = multiline(function() {/* 
      var Out = "";
      sky6RASCOMTele.Connect();
      if (sky6RASCOMTele.IsConnected == 0) {
        Out = "Not connected";
      } else {
        sky6RASCOMTele.Asynchronous = 0;
        sky6RASCOMTele.Abort();
        sky6RASCOMTele.SlewToAzAlt($az, $alt, 'altaz_coords');
        while(!sky6RASCOMTele.IsSlewComplete) {
          sky6Web.Sleep(1000);
        }
        Out = "Slew to Alt-Az complete.";
      }
    */});
    javascript = javascript.replace('$alt', alt);
    javascript = javascript.replace('$az', az);
    javascript = "/* Java Script */\n" + javascript;
  });

program
  .command('take <time>')
  .description('take an image with ccd using exposure time')
  .action(function(time, options) {
    javascript = multiline(function() {/* 
      var path = "/Users/SohrabZ/Desktop/fits/";
      ccdsoftCamera.AutoSaveOn = true;
      ccdsoftCamera.AutoSavePath = path;
      ccdsoftCamera.CameraExposureTime = $time;
      // Take the image
      ccdsoftCamera.Autoguider = false;
      ccdsoftCamera.Asynchronous = false;
      if (ccdsoftCamera.Connect()) {
        Out = "Not connected";
        return;
      } else {
        ccdsoftCamera.Abort();
        while (ccdsoftCamera.State != 0) {
          sky6Web.Sleep(1000);
        }
        ccdsoftCamera.ImageReduction = 0;
        ccdsoftCamera.TakeImage();
        while (ccdsoftCamera.State != 0) {
          sky6Web.Sleep(1000);
        }
        var fileName = ccdsoftCamera.LastImageFileName;
        Out = "Image taken|Location: " + fileName;
      }
    */});
    javascript = javascript.replace('$time', time);
    javascript = "/* Java Script */\n" + javascript;
  });

program
  .command('home')
  .description('slews telescope to home position')
  .action(function(options) {
    javascript = multiline(function() {/* 
      var Out;
      var Err;
      sky6RASCOMTele.Connect();
      if (sky6RASCOMTele.IsConnected == 0) {
        Out = "Not connected";
      } else {
        sky6RASCOMTele.Abort();
        sky6RASCOMTele.FindHome();
        while(!sky6RASCOMTele.IsSlewComplete) {
          sky6Web.Sleep(1000);
        }
        Out = "Mount homed. LastSlewError: "+sky6RASCOMTele.LastSlewError;
      };
    */});
    javascript = "/* Java Script */\n" + javascript;
  });

program
  .command('park')
  .description('slews telescope to park position')
  .action(function(options) {
    javascript = multiline(function() {/* 
      var Out;
      sky6RASCOMTele.Connect();
      if (sky6RASCOMTele.IsConnected==0) {
        Out = "Not connected";
      } else {
        sky6RASCOMTele.Asynchronous = 0;
        sky6RASCOMTele.Abort();
        sky6RASCOMTele.Park();
        while(!sky6RASCOMTele.IsSlewComplete) {
          sky6Web.Sleep(1000);
        }
        Out = "Mount parked. LastSlewError: "+sky6RASCOMTele.LastSlewError;
      };
    */});
    javascript = "/* Java Script */\n" + javascript;
  });

program
  .command('purge')
  .description('purges the serial port')
  .action(function(options) {
    javascript = multiline(function() {/* 
      sky6RASCOMTele.Connect();
      if (sky6RASCOMTele.IsConnected == 0) {
        Out = "Not connected"
      } else {
        sky6RASCOMTele.Abort();
        sky6RASCOMTele.DoCommand(0,"dummy");
        sky6RASCOMTele.DoCommand(1,"dummy");
        sky6RASCOMTele.DoCommand(2,"dummy");
        sky6RASCOMTele.DoCommand(6,"dummy");
        Out = "Serial port purged"; 
      };
    */});
    javascript = "/* Java Script */\n" + javascript;
  });

program
  .command('start')
  .description('starts telescope tracking')
  .action(function(options) {
    javascript = multiline(function() {/* 
      var Out;
      sky6RASCOMTele.Connect();
      if (sky6RASCOMTele.IsConnected == 0) {
        Out = "Not connected";
      } else {
        sky6RASCOMTele.Abort();
        sky6RASCOMTele.SetTracking(1,1,0,0);
        Out = "Mount tracking at sidereal rate. LastSlewError: "+sky6RASCOMTele.LastSlewError;
        Out += "|Track: " + sky6RASCOMTele.IsTracking;
       };
    */});
    javascript = "/* Java Script */\n" + javascript;
  });

program
  .command('stop')
  .description('stops telescope tracking')
  .action(function(options) {
    javascript = multiline(function() {/* 
      var Out;
      sky6RASCOMTele.Connect();
      if (sky6RASCOMTele.IsConnected == 0) {
        Out = "Not connected";
      } else {
        sky6RASCOMTele.Abort();
        sky6RASCOMTele.SetTracking(0,1,0,0);
        Out = "Mount tracking off. LastSlewError: "+sky6RASCOMTele.LastSlewError;
        Out += "|Track: " + sky6RASCOMTele.IsTracking;
      };
    */});
    javascript = "/* Java Script */\n" + javascript;
  });

program.parse(process.argv);

function checkTheSkyX(callback) {
  pid = execSync("ps -ef | grep TheSkyX | grep -v grep|awk '{print $2}'", { encoding: 'utf8' });
  started = false;
  
  if(!pid) {
    if(program.verbosity) {
      console.log('LOG :: Opening TheSkyX');
    }
    
    exec('nohup /home/shekarchi/SKYX-MOUNT/TheSkyX/TheSkyX &> /dev/null &', function(err, stdout, stderr) {
      if (err) throw err;
    });
    pid = execSync("ps -ef | grep TheSkyX | grep -v grep|awk '{print $2}'", { encoding: 'utf8' });
    started = true;
  }

  // Make sure the callback is a function​
  if (typeof callback === "function") {
    callback(pid.trim(), started);
  }
}

function sendJavaScript(javascript, callback) {
  fs.writeFileSync('/var/tmp/tmp.js', javascript, { encoding: 'utf8' });
  output = execSync('node ' + __dirname + '/skysend.js localhost /var/tmp/tmp.js', { encoding: 'utf8' });

  // Make sure the callback is a function​
  if (typeof callback === "function") {
    callback(output.trim());
  }
}

checkTheSkyX(function(pid, started) {
  if(program.verbosity) {
    console.log('LOG :: TheSkyX is running with process id of %s', pid);  
  }

  if(started == true) {
    // wait for the sky x to be fully functional
    sleep.sleep(5);
  }
});

if(javascript.length != 0) {
  sendJavaScript(javascript, function(output) {
    console.log(output);
  });
} else {
  console.log("Command not found !");
}

process.exit(1);
