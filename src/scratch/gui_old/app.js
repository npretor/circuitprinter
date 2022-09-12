/* 


currently the video server is in: 
~/scratch/h264-live-player/server-rpi.js 
*/

const express = require('express')
const fs = require('fs')
//const glob = require('glob')
const app = express()
const port = 80

app.use(express.static('public'));
app.use(express.static(__dirname + "/public"));
// console.log(__dirname);
app.use(express.static(__dirname + '/static'));

/*
Working streamer
sudo apt-get install gstreamer1.0-tools
raspivid -t 999999 -h 720 -w 1280 -fps 25 -b 2000000 -vf -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=0.0.0.0 port=8554

Trying this: 
https://raspberrypi.stackexchange.com/questions/42881/how-to-stream-low-latency-video-from-the-rpi-to-a-web-browser-in-realtime

https://github.com/131/h264-live-player
*/


// - - - - - - - Setup express to use html - - - - - - - //
app.set('views', __dirname);
app.engine('html', require('ejs').renderFile); 
//app.set('view engine', 'ejs'); 


// - - - - - - - Routing - - - - - - - //
app.get('/', (req, res) => {
  res.render('index.html')
});

app.get('/tool_calibration', function (req, res)
{
    res.render('tool_calibration.html');
});

app.get('/fiducials', function (req, res)
{
    res.render('align_artwork.html');
});

app.get('/print', function (req, res)
{
    res.render('print.html');
});


// - - - - - - - Stuff in the background  - - - - - - - //
app.get('/print_cal_pattern', function (req, res)
{
    console.log('printing calibration pattern')
    // Send a signal to print a dxf or gcode crosshair centered at a known absolute location
    //printCrosshair()
});

// - - - - - - - Server startup - - - - - - - //
app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
});