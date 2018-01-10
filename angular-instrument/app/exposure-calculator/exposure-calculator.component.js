'use strict';

// Register `exposureCalculatorOptionFilter` component, along with its associated controller and template
//angular.
//module('exposureCalculatorOptionFilter').
//component('exposureCalculatorOptionFilter', {
//    templateUrl: 'exposure-calculator/exposure-calculator.template.html',
//    controller: ['availablefilter',
//        function filterListController(availablefilters) {
//            this.availablefilters = instrumentoptions.query();
//        }
//    ]
//})

// Register `exposureCalculator` component, along with its associated controller and template
angular.
module('exposureCalculator').
component('exposureCalculator', {
    templateUrl: 'exposure-calculator/exposure-calculator.template.html',
    controller: [
        function() {
            var self = this;

            // default setting
            self.selectedinstrument = "ioo";
            self.selectedbinning = "two";
            self.selectedfilter = "fbb";

            self.calculateImaging = function(inputValue, instrum, binn, filt) {

                var mag = parseFloat(inputValue.val1),
                    snr = parseFloat(inputValue.val2);

                var w = window,
                    d = document,
                    e = d.documentElement,
                    g = d.getElementsByClassName('exposureTime')[0];

                var margin = {
                    top: 20,
                    right: 40,
                    bottom: 20,
                    left: 20
                };

                var headWidth = 320,
                    cellWidth = 80,
                    cellHeight = 40;

                var width = (w.innerWidth || e.clientWidth || g1.clientWidth) - margin.right - margin.left;

// THIS IS NOT AN ANGULARJS WAY OF CONSTRUCTING A PULL-DOWN BAR, THIS IS COPIED FROM THE SCRIPT ON THE CURRENT LT WEB PAGE.

                // FIRST PULL-DOWN ***   
                // Look-up tables of variables - INSTRUMENT CHARACTERISTICS
                    if (instrum == "ioo")         {     
                var pixscale = 0.15;
                var darkcurrent = 0;
                var readnoise = 10;
                    } else if (instrum == "ioi")  {
                      var pixscale = 0.18;     
                      var darkcurrent = 0;   
                      var readnoise = 17;   
                    } else if (instrum == "rise") {
                      var pixscale = 0.54;     
                      var darkcurrent = 0;   
                      var readnoise = 10;    
                    } else                       { // ringo3
                      var pixscale = 0.48;   
                      var darkcurrent = 0;   
                      var readnoise = 17;  // Updated by IAS via NRC October 2015
                    };  

                // SECOND PULL-DOWN ***
                // Look-up tables of variables -BINNING
                    if (binn == "two") {    
                      var bin = 2;
                    } else            {  
                      var bin = 1;
                    };

                // THIRD PULL-DOWN ***
                // Look-up tables of variables - ZERO POINTS & SKY (inst and filter specific)
                // NB. ZPs should correspond to 1 electron/second (i.e. corrected for GAIN)
                // The RINGO3 values assume GAIN = 1, and therefore become increasingly 
                // inaccurate at exposure times >3 sec.
                // For skybrightness data see:
                //     http://www.ing.iac.es/Astronomy/observing/conditions/skybr/skybr.html
                // ...
                    if (filt == "fsu") {            // IO:O sdss_u
                      var zp = 22.17;               // 21.30 from old ETC, modified by CMC in Jan 2016 using Helen Jermak's post-recoating factors (29 June 2015 email)
                      var skybr = 21.0;             // Skybr values are similar to ING
                      var skyoff = 1.5;             //   measurements on their web-site    
                    } else if (filt == "fbb") {     // IO:O bessell_b
                      var zp = 24.90; 				// 24.10 from old ETC, modified with HJ's factor
                      var skybr = 22.3; 
                      var skyoff = 1.5;
                    } else if (filt == "fbv") {     // IO:O bessell_v
                      var zp = 24.96; 				// 24.20 from old ETC, modified with HJ's factor
                      var skybr = 21.4; 
                      var skyoff = 1.5;
                    } else if (filt == "fsg") {     // IO:O sdss_g
                      var zp = 25.14; 				// 24.40 from old ETC, modified with HJ's factor
                      var skybr = 21.7; 
                      var skyoff = 1.0;
                    } else if (filt == "fsr") {     // IO:O sdss_r
		        var zp = 25.39; // 24.60 from old ETC, modified with HJ's factor
		        var skybr = 20.4;
		        var skyoff = 1.0;
                    } else if (filt == "fsi") {     // IO:O sdss_i
                      var zp = 25.06; 				// 24.40 from old ETC, modified with HJ's factor
                      var skybr = 19.3; 
                      var skyoff = 1.0;
                    } else if (filt == "fsz") {     // IO:O sdss_z
                      var zp = 24.52; 				// 24.0 from old ETC, modified with HJ's factor
                      var skybr = 18.3; 
                      var skyoff = 0.5;     
                    } else if (filt == "fjj") {      // IO:I J-band
                      var zp = 24.50;     // 24.0 from IO:I webpage (pre-commissioning, so RMB estimate?). In Jan 2016 CMC added 0.5 after 2015 recoating.
                      var skybr = 16.6;   // from ING sky brightness page, in mag per sqr arcsec
                      var skyoff = 0.0;   // skyoff assumes moon has no affect on J-band sky
                    } else if (filt == "fhh") {      // IO:I H-band
                      var zp = 24.00;     // 23.5 updated after commissioning; corrected for gain (CJD). CMC added 0.5 after 2015 recoating.
                      var skybr = 12.5;   // from ING sky brightness page, in mag per sqr arcsec
                      var skyoff = 0.0;   // skyoff assumes moon has no affect on H-band sky    
                    } else if (filt == "frise")  {   // rise  V+R
                      var zp = 25.20;     // In Jan 2016 CMC added 0.7 to original value of 24.50 following 2015 recoating
                      var skybr = 20.4;   // ... same as sdss-r above
                      var skyoff = 1.0;   // ... same as sdss-r above
                    } else if (filt == "frise720")  {   // rise 720
                      var zp = 23.40;     // 
                      var skybr = 19.3;   // ... same as sdss-i above
                      var skyoff = 1.0;   // ... same as sdss-i above
                    } else if (filt == "fringr") {   // ringo3 (red 'd')   - assume like I
                      var zp = 21;         // Updated by IAS via NRC October 2015
                      var skybr = 19.3;    // ... same as sdss-i above
                      var skyoff = 1.0;    // ... same as sdss-i above
                    } else if (filt == "fringg") {   // ringo3 (green 'f') - assume like R
                      var zp = 21.8;       // Updated by IAS via NRC October 2015
                      var skybr = 20.4;    // ... same as sdss-r above 
                      var skyoff = 1.0;    // ... same as sdss-r above
                    } else                       {   // ringo3 (blue 'e')  - assume like B
                      var zp = 23;         // Updated by IAS via NRC October 2015
                      var skybr = 22.3;    // ... same as bessel B above 
                      var skyoff = 1.5;    // ... same as bessel B above
                    };

                // *************************************************************************

                // **** 
                // **** Check the select-option combinations are valid
                // ****

                //IO:O
                    if (instrum == "ioo" && binn == "rgbin") {
                        alert("Incorrect Instrument-Binning Combination!");
                    }
                    if (instrum == "ioo" && filt == "fjj") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ioo" && filt == "fhh") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ioo" && (filt == "frise" || filt == "frise720") ) {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ioo" && filt == "fringr") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }    
                    if (instrum == "ioo" && filt == "fringg") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }    
                    if (instrum == "ioo" && filt == "fringb") {
                        alert("Incorrect Instrument-Filter Combination!");
                    } 

                //IO:I
                    if (instrum == "ioi" && binn == "rgbin") {
                        alert("Incorrect Instrument-Binning Combination!");
                    }
                    if (instrum == "ioi" && filt == "fsu") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ioi" && filt == "fbb") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ioi" && filt == "fbv") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ioi" && filt == "fsg") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ioi" && filt == "fsr") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ioi" && filt == "fsi") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ioi" && filt == "fsz") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ioi" && (filt == "frise" || filt == "frise720") ) {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ioi" && filt == "fringr") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ioi" && filt == "fringg") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ioi" && filt == "fringb") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }

                //RISE
                    if (instrum == "rise" && binn == "rgbin") {
                        alert("Incorrect Instrument-Binning Combination!");
                    }
                    if (instrum == "rise"){
                        if ( !(filt == "frise" || filt == "frise720") ) {
                            alert("Incorrect Instrument-Filter Combination!");
                        }
                    }

                //RINGO3
                    if (instrum == "ringo" && binn == "one") {
                        alert("Incorrect Instrument-Binning Combination!");
                    }
                    if (instrum == "ringo" && binn == "two") {
                        alert("Incorrect Instrument-Binning Combination!");
                    }
                    if (instrum == "ringo" && filt == "fsu") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ringo" && filt == "fbb") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ringo" && filt == "fbv") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ringo" && filt == "fsg") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ringo" && filt == "fsr") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ringo" && filt == "fsi") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ringo" && filt == "fsz") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ringo" && filt == "fjj") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ringo" && filt == "fhh") {
                        alert("Incorrect Instrument-Filter Combination!");
                    }
                    if (instrum == "ringo" && (filt == "frise" || filt == "frise720") ) {
                        alert("Incorrect Instrument-Filter Combination!");
                    }

                // Could display in table the ZP to be used - commented out below
                // document.getElementById("zpused").innerHTML = zp.toFixed(2); 

                // *************************************************************************

                // ****
                // **** MAIN CALCULATION (Imaging)
                // ****

                // POINT sources
                // Calculate exposure times based on a range of seeing and sky brightness
                // values.
                // Step through seeing and sky brightness (nested for loops).  
                //    - seeing is 1.0 when i=1; step by 0.5 arcsec so seeing is 4.0 when i=7 
                //    - sky bright is Dark when j=0; step by 1 mag so sky is dark+10 when j=10 
                // Output values stored in a 1-D variable (2D a pain to code)

                var skymaglist = [0.0, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 4.0, 6.0, 10.0],
                    seeinglist = [0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 4.0];

                // calculate the sky magnitude
                skymaglist = skymaglist.map(function(element) {
                    return skybr - (skyoff * element);
                });

                // calculate (approximate) the area of the psf disk
                var areaofdisklist = seeinglist.map(function(element) {
                    return 2.0 * element * 2.0 * element;
                });

                //  - skyoff takes into account 1 mag change in 
                //    V doesn't equal 1 mag change in u or r.              

                var itot = skymaglist.length,
                    jtot = seeinglist.length;

                // sets up texp as an ARRAY 
                var texp = new Array(itot+1);

                for (i=0; i<itot+1; i++) {
                    texp[i] = new Array(jtot+1)
                }

                var snr2 = snr * snr;

                var pixescalecorrection = pixscale * pixscale * bin * bin;
                var starphotons = Math.pow(10.0, ((zp - mag) / 2.5)); // within aperture

                var header = ["Sky \\ Seeing ", "0.75\"", "1.0\"", "1.25\"", "1.5\"", "1.75\"", "2.0\"", "2.5\"", "3.0\"", "4.0\""],
                    rowhead = ["Dark", "Dark + 0.5 mag", "Dark + 0.75 mag", "Dark + 1.0 mag", "Dark + 1.25 mag", "Dark + 1.5 mag", "Dark + 2.0 mag", "Dark + 4.0 mag", "Dark + 6.0 mag", "Dark + 10.0 mag"];

                texp[0] = header;

                for (var i=1; i<itot+1; i++) {

                    texp[i][0] = rowhead[i-1];
                    var skymag = skymaglist[i-1];

                    for (var j=1; j<jtot+1; j++) {

                        // Get the disk area in arcsec^2
                        var areaofdisk = areaofdisklist[j-1];

                        // Sky photons within aperture
                        var skyphotons = Math.pow(10.0, ((zp - skymag) / 2.5)) * areaofdisk;

                        // Find the area in pixels
                        //  - must multiply by areaofdisk since skymag 
                        //    in mag/arcsec2 
                        var numberofpixels = areaofdisk / pixescalecorrection;

                        var a = starphotons * starphotons,
                            b = -snr2 * (starphotons + skyphotons + darkcurrent),
                            c = -snr2 * numberofpixels * readnoise * readnoise;
                        var delta = Math.sqrt(b*b - 4.0*a*c)
                        var texpaa = (-b + delta) / (2.0*a); // solve quadratic equation (+ve)
                        var texpbb = (-b - delta) / (2.0*a); // solve quadratic equation (-ve)           

                        texp[i][j] = Math.max(texpaa, texpbb); // select greater value

                        // Check for exposure time is <1 sec or >3 hr, or if saturation likely
                        var test = texp[i][j];
                        if (test < 1.0) {
                            texp[i][j] = 1;
                        }
                        if (test > 99999.0) {
                            texp[i][j] = 99999;
                        }
                        if ((starphotons * test / numberofpixels) > 10000.0) {
                            texp[i][j] *= -1;
                        }

                    }
                }

                // EXTENDED sources
                // SAME CALCULATION (but for extended sources) 
                // Calculate exposure times based on a range of sky brightness values
                // Step through sky brightness.  
                //    - sky brightness is Dark when j=0; sky is dark+10 when j=10 
                // Output values stored in another 1-D variable (2D a pain to code)

                var cellex = 1;
                var texpex = []; // sets up texpex as an ARRAY 
                var numberofpixels = 1.0 / pixescalecorrection; // pixels in 1 arcsec
                var starphotons = Math.pow(10.0, ((zp - mag) / 2.5)); // within 1x1 arcsec
                for (var j = 0; j <= 10; j++) {

                    var skymag = skybr - (skyoff * j);

                    var skyphotons = Math.pow(10.0, ((zp - skymag) / 2.5)); // within 1x1 arcsec

                    var a = starphotons * starphotons,
                        b = -snr2 * (starphotons + skyphotons + darkcurrent),
                        c = -snr2 * numberofpixels * readnoise * readnoise, // Readnoise per sqr arc
                        delta = Math.sqrt(b * b - 4.0 * a * c);

                    var texpexaa = (-b + delta) / (2.0 * a),
                        texpexbb = (-b - delta) / (2.0 * a);
                    texpex[cellex] = Math.max(texpexaa, texpexbb);

                    // Same check for sub-1-sec exp times, >3 hr exp times, and saturation
                    var test = texpex[cellex];

                    if (test < 1.0) {
                        texpex[cellex] = 1;
                    }
                    if (test > 99999.0) {
                        texpex[cellex] = 99999;
                    }
                    if ((starphotons * test / numberofpixels) > 10000.0) {
                        texpex[cellex] *= -1;
                    }

                    cellex++;
                }


                var colorScale = d3.scale.threshold()
                    .domain([1.0, 600.0, 10800.0, 21600.0])
                    // < 10 minutes:         LJMU Green #C7D401
                    // 10 minutes - 3 hours: Bright Gold #FDD017
                    // > 3 hours:            Pinterest Red #C8232C
                    .range(["#CCCCCC", "#C7D401", "#FDD017", "#C8232C", "#888888"]);

                var table = d3.select('.exposureTime')
                    .select('table')

                var rows = table.selectAll('tr')
                    .data(texp)
                    .enter()
                    .append('tr')


                var cells = rows.selectAll('td')
                    .data( function (row) {
                        //console.log(row);
                        return row.map( function (column) {
                            //console.log(column);
                            return column;
                        });
                    })
                    .enter()
                    .append('td')
                    .attr('align', "center")
// deprecated                     .attr('width', function(d) {
//                        if ( isNaN(d) ) {
//                           return headWidth;
//                        } else {
//                            return cellWidth;
//                        }
//                    })
//                    .attr('height', cellHeight)

                d3.selectAll('tr')
                    .data(texp)
                    .selectAll('td')
                    .data( function (row) {
                        //console.log(row);
                        return row.map( function (column) {
                            //console.log(column);
                            return column;
                        });
                    })
                    .text(function (d) {
//                        console.log(d);
                        if ( isNaN(d) ) {
                            return d
                        } else {
                            return Math.round(Math.abs(d));
                        }
                    })
                    .attr('bgcolor', function(d) {
                        if ( isNaN(d) ) {
                            return "#EDEDED"
                        } else {
                            return colorScale(d);
                        }
                    })


            }
        }
    ]
});
