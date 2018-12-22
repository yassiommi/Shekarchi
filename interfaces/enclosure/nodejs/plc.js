#!/usr/bin/env node

var plc  = require("plc");

var args = process.argv.slice(2);
var enclosureOpen = false;
var enclosureClose = false;
var variableName = "";
var marker = 0;

if (args[0] == "open") {
	variableName = "enclosureOpen";
	marker = 1;
} else if (args[0] == "close") {
	variableName = "enclosureClose";
	marker = 0;
} else {
	console.log("missing argument 1 !");
	console.log("use open or close as the first argument");
	process.exit(1);
}

var myLogo = new plc.Logo("10.143.44.59", {
	timeout: 1000  // socket timeout in milliseconds 
});

myLogo.on("error", function(err) {
	console.error(err.message);
});

myLogo.on("connect", function() {
  var i = 0;

  // clear markers
  result = myLogo.clearMarker(0);
  
  if (result instanceof Error) {
    return console.error(result.message);
  }

  result = myLogo.clearMarker(1);
  
  if (result instanceof Error) {
    return console.error(result.message);
  }

  // set the marker to true
  console.log("setting marker to true");
  
  result = myLogo.setMarker(marker);
  
  if (result instanceof Error) {
    return console.error(result.message);
  }

  console.log("marker is true");

	console.log("waiting for status to change");
	while (eval(variableName) == false) {
		if (i%2500000 == 0) {
			var result = myLogo.getInputs();

			if (result instanceof Error) {
				return console.error(result.message);
			}
			
			enclosureOpen = result[2];
			enclosureClose = result[3];
		}

		i++;
	}
	console.log("status is changed");

  // clear marker
  console.log("clearing marker");
  
  result = myLogo.clearMarker(marker);
  
  if (result instanceof Error) {
    return console.error(result.message);
  }

  console.log("marker is cleared");

	myLogo.disconnect();
});

myLogo.connect();

myLogo.on("disconnect", function() {
	if (variableName == "enclosureOpen") {
		console.log("Enclosure is opened");
	} else {
		console.log("Enclosure is closed");
	}
});
