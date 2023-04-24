"""
Nathan Pretorius 2022


"""


import json 
import time
import zmq
import logging    


class MotionClient: 
    """

    """
    def __init__(self, serial_port='/dev/ttyACM0', address='127.0.0.1', socket_port=5678):
        self.serial_port = serial_port 
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://{}:{}".format(address, socket_port))  

    def send(self, message):
        self.socket.send(message.encode())
        return(self.socket.recv().decode())
    
    def sendJson(self, json_message):
        return self.send(json.dumps(json_message)) 

    def gcode(self, message):
        return self.send(json.dumps({'gcode': message})) 
    
    def connect(self):
        return self.send(json.dumps({'connect': True}) )

    def disconnect(self):
        return self.send(json.dumps({'connect': False}) )

    def close(self):
        self.socket.close()  

    def position(self):
        json_res = self.gcode('M114') 
        res = json.loads(json_res)['res'] 
        strings = res.split(' ') 
        locations = [float(item[2:]) for item in strings[0:3]] 
        return locations 