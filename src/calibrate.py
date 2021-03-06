""" 
WHAT DID WE LEARN TODAY: We need a gui for the motion control, can't jump between serial control and web control
"""


import json 
import time 
import io
import picamera
import logging
import os 
import subprocess
import socketserver
from threading import Condition
from http import server
from hardware.DuetController import DuetController
from hardware.LightController import LightController


print('First verify that the machine has been homed and a syringe is mounted with a tip')

PAGE="""\
<html>
<head>
<title>picamera MJPEG streaming demo</title>
</head>
<body>
<h1>PiCamera MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

# - - - - - - - Initialize hardware - - - - - - - #
motion = DuetController()
motion.connect()
#light = LightController()
#light.on()

# - - - - - - - Open machine config file - - - - - - - #
with open('config/machine_settings.json') as f:
    m_settings = json.load(f)

global cPos
global t1Pos

# - - - - - - - Camera calibration - - - - - - - #
def cameraCalibration_withServer():
    with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
        flag = 0
        output = StreamingOutput()
        camera.start_recording(output, format='mjpeg')
        try:
            address = ('', 8000)
            server = StreamingServer(address, StreamingHandler)
            server.serve_forever()
        finally:
            camera.stop_recording()
            print('Camera server stopped')

        print('Go to http://localhost.8000 to view camera in one window')
        print('Go to http://192.168.4.47 to view motion control in a second window')

        print(' ################################################')
        print(' ####  Now move to the correct location #########')
        print(' ####  When at the location hit the s key #########')
        while flag == 0: 
            inp = input("Press s when ready to save location: ")
            print('You pressed: {}'.format(inp))
            if inp == 's':
                flag = 1
        print('Saving location now')
    return 1

def parsePosition(): 
    positionString = motion.get_absolute_position()
    locations = positionString.split()
    xPos = float(locations[0][2:])
    yPos = float(locations[1][2:])
    zPos = float(locations[2][2:])
    #print('Current position:  {} {} {}'.format(xPos, yPos, zPos))
    return [xPos, yPos, zPos]

def cameraCalibration():
    flag = 0
    print('Go to http://localhost.8000 to view camera in one window')
    print('Go to http://192.168.4.47 to view motion control in a second window')
    motion.disconnect()
    print(' ################################################')
    print(' ####  Now move to the correct location #########')
    print(' ####  When at the location hit the s key #######')
    print(' ################################################')
    while flag == 0: 
        inp = input("Press s when ready to save location: ")
        print('You pressed: {}'.format(inp))
        if inp == 's':
            flag = 1
    print('Saving location now')   
    motion.connect()
    cPos = parsePosition()
    return(cPos)
    # G0 X267.9 Y72.3 Z14.0

# - - - - - - - Tool calibration - - - - - - - #
def toolCalibration(tool=1):
    flag = 0
    print('Picking up the tool')
    motion.send('T{}'.format(tool-1))
    motion.disconnect()
    print(' ################################################')
    print(' ####  Now move to the correct location #########')
    print(' ####  When at the location hit the s key #######')
    print(' ################################################')
    while flag == 0: 
        inp = input("Press s when ready to save location: ")
        print('You pressed: {}'.format(inp))
        if inp == 's':
            flag = 1
    motion.connect()
    tPos = parsePosition()
    return(tPos)



cPos = cameraCalibration()
print('Position: {} {} {}'.format(cPos[0], cPos[1], cPos[2]))
time.sleep(2)

t1Pos = toolCalibration(1)
print('Position: {} {} {}'.format(t1Pos[0], t1Pos[1], t1Pos[2]))

print('The camera is the zero point, so we will subtract from that')
print('Tool 0 offset from camera: Z{} Z{} Z{}'.format(cPos[0]-t1Pos[0], cPos[1]-t1Pos[1], cPos[2]-t1Pos[2]))

motion.disconnect()
#light.off()
