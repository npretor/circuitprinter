"""
Nathan Pretorius 2022


"""


import json 
import time
import zmq
import logging    

logging.basicConfig(level=logging.INFO)

class MotionClient: 
    """
    Connects to MotionServer. Manages connections and 
    """
    def __init__(self, serial_port='/dev/ttyACM0', address='127.0.0.1', socket_port=5678):
        """
        Initialize and bind to address and port. 
        TODO : Get the serial port setup working, it's broken right now and the port changes 
        """
        self.serial_port = serial_port 
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://{}:{}".format(address, socket_port))  

    def send(self, message):
        """Core socket send-receive functionality"""
        self.socket.send(message.encode())
        return(self.socket.recv().decode())
    
    def sendJson(self, json_message):
        """Accepts json, converts to string and sends"""
        return self.send(json.dumps(json_message)) 
    
    # Camera-specific requests 
    def start_camera(self):
        return self.send(json.dumps({'start_camera': True}))     
    
    def stop_camera(self):
        return self.send(json.dumps({'stop_camera': True}))             

    def save_image(self, image_name):
        """This should save an image on the server side, to be retrieved later"""
        return self.send(json.dumps({'save_image': image_name})) 

    def send_image(self):
        """ Send an image to the zmq client"""
        return self.send(json.dumps({'send_one_image': True})) 

    def cache_status(self):
        return self.send(json.dumps({'cache_status': True})) 

    # Motion-specific requests
    def gcode(self, message):
        """Adds a gcode command to correct json formatting for MotionServerZMQ parser"""
        return self.send(json.dumps({'gcode': message})) 

    def connect(self, test_mode):
        """Send a connection command. Starts serial connection to hardware"""
        return self.send(json.dumps({'connect': True, 'test_mode': test_mode}) )

    def disconnect(self):
        """Closes serial connection to hardware"""
        return self.send(json.dumps({'connect': False}) )

    def position(self):
        """Send get position command and parse"""
        json_res = self.gcode('M114') 
        res = json.loads(json_res)['res'] 
        strings = res.split(' ') 
        locations = [float(item[2:]) for item in strings[0:3]] 
        return locations 

    # Close 
    def close(self):
        """Close socket connection to MotionServerZMQ"""
        self.socket.close()          