/* 
Pages
    - Simple Print > Register > Status
    - Registered print > Register > Status
    - Calibrate 
    - Settings

Simple print
- Start new project name
    - Input name
    - Upload file
    - Select ink and associated tools
- Load DXF and read with name L1
    - Display layers visually with colors 
    - Select a layer to print
- Test print 
    - (Later) measure with camera
*/

const express = require('express')
const path = require('path');
const fs = require('fs')
const ejs = require('ejs')
const glob = require('glob')
const os = require('os');
const multer  = require('multer');
var zmq = require("zeromq");
const { error } = require('console');
const { connect } = require('http2');
const upload = multer({ dest: 'temp/' });
const app = express()
const port = 80


/* - - - - - - - - - Setup - - - - - - - - - */
// https://stackoverflow.com/questions/5710358/how-to-access-post-form-fields
app.use(express.json());       // to support JSON-encoded bodies
app.use(express.urlencoded({ extended: true })); // to support URL-encoded bodies 

// - - - - - - - Setup express to use html - - - - - - - // 
app.set('views', __dirname + '/views');
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'ejs');

function readJsonFile(filename){
    let rawdata = fs.readFileSync(filename);
    let data = JSON.parse(rawdata);
    return data
}

// Read the settings file
//settings = readJsonFile('../config/settings.json')

function zmq_connect(address, port) {
    console.log('Attempting to connect') 
    sock = zmq.createSocket('req'); 
    sock.connect("tcp://" + address + ":" + port, function(error){
        console.log('connected?')
        if (error){
            console.log("Error connecting: ", error)
        } else {
            console.log("Connected to: ", address, "  ", port); 
        } 
    }); 
    return sock
} 

motion_server = zmq_connect('127.0.0.1', '5555') 

// - - - - - - - Routing - - - - - - - //
// - - - - - - - Print
app.get('/', (req, res) => {
    res.render('pages/home');
});
app.post('/', (req, res) => {
    console.log(req.body);
    res.render('pages/home');
});

app.get('/simple_print', (req, res) => {
    ink_names = ['Primary Conductive - ACI 3214', 'Primary Adhesive - ACI 3331']
    res.render('pages/simple_print', {
        ink_names
    });
});
app.post('/simple_print', (req, res) => {
    ink_names = ['Primary Conductive - ACI 3214', 'Primary Adhesive - ACI 3331']
    res.render('pages/print_status', {
        ink_names
    });
});

app.get('/registered_print', (req, res) => {
    ink_names = ['Primary Conductive - ACI 3214', 'Primary Adhesive - ACI 3331']
    res.render('pages/registered_print', {
        ink_names
    });
});
app.post('/registered_print', (req, res) => {
    console.log()
    res.render('pages/print_status', {
        ink_names
    });
});

app.get('/print_status', (req, res) => {
    res.render('pages/print_status');
});

app.get('/settings', (req, res) => {
    res.render('pages/settings');
});

app.get('/tool_calibration', function(req, res){
    //console.log('saving the current location');
    // Code to get the location goes here. The server should is a service we request using zmq
    res.render('pages/tool_calibration');
}); 
app.post('/tool_calibration', (req, res) => {
    tool = 'air_extruder'
    console.log(req.body)

    // Connect to motion server
    // Move relative 
    if ("x_value" in req.body){ 
      console.log("Sending move X relative : ",req.body.x_value) 
      message = JSON.stringify({"moveRel": [req.body.x_value, 0.0, 0.0]}) 
      console.log(message) 
      motion_server.send(message) 
    } 
    else if ("y_value" in req.body){
      console.log("Sending move Y relative: ",req.body.y_value)
      message = JSON.stringify({"moveRel": [0.0, req.body.y_value, 0.0]})
      console.log(message) 
      motion_server.send(message)     
    } 
    else if ("z_value" in req.body){
      console.log("Sending move Z relative: ",req.body.z_value)
      message = JSON.stringify({"moveRel": [0.0, 0.0, req.body.z_value]})
      console.log(message) 
      motion_server.send(message) 
    } else if ("getPosition" in req.body){
      console.log("Saving home location for tool: ",req.body.toolName) 
      // Get the home location 
      // Save to settings 
    } else { 
      console.log('Key not found: ', req.body) 
    } 
    res.render('pages/tool_calibration', {
        tool
    });
});


// - - - - - - - Start server - - - - - - - //
app.listen(port, () => {
    console.log(`App live at http://localhost:${port}`)
  });