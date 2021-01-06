# To run: 
#   export FLASK_APP=flask_video.py
#   flask run

from camera import Camera
from flask import Flask, send_file
app = Flask(__name__)

cam = None

# State checks to prevent multiple initialization
def check_cam():
    global cam
    if cam == None:
        print('starting camera')
        cam = Camera()
        cam.open()


index = ''' <html>
    <head>
    </head>
    <body>
    <h1> Video should be here</h1>
    <!--
        <video width="640" height="480" controls>
            <source src="movie.h264" type="video/mp4">
        Your browser does not support the video tag.
        </video>
    -->
        <div id="preview">
            <img id="preview_image" width=100%>
        </div>
    </body>
    <!-- <script src="cam_preview.js"><script> -->
    <script> 
        "use strict";
        (function reload_image() {
        console.log('reload_image was run')
        var url = '/cam_image'
        fetch(url, {cache: "no-store"}).then(function(response) {
            if(response.ok) {
            response.blob().then( function(blob) {
                console.log('camPreview was run')
                var objectURL = URL.createObjectURL(blob);
                var img = document.getElementById('preview_image');
                img.src = objectURL;
                setTimeout (reload_image, 500);
            });
            } else {
            console.log('Network request for camera image failed with response ' + response.status + ': ' + response.statusText);
            }
        });
        })();

    </script> 
</html>
'''

@app.route('/')
def hello_world():
    print('hi, you are on the root page')
    return index

@app.route('/cam_image')
def cam_image():
    global cam
    print('should run check_cam after this')
    check_cam()
    image_stream = cam.capture_stream()
    return send_file(image_stream, mimetype='image/png') 