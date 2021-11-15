"""
This client accepts these commands: 
    moveRelative
    moveAbsolute
    Home
    HomeXY
    getLocation

It returns these: 
    1:  command executes correctly 
    0:  command failed
    2:  out of bounds location or speed
    location in XYZ: (X, Y, Z)

Example command: 
{
    "moveRel": {
        "x", 10.0, 
        "y", 10.0, 
        "z", 10.0, 
        "speed": 20.0
    }
}
"""


import json 
import time
import zmq
import logging

PORT = 5555        # Port to listen on (non-privileged ports are > 1023)

SERVER_ADDR = '127.0.0.1'

class MotionClient: 
    def __init__(self, SERVER_ADDR):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://{}:{}".format(SERVER_ADDR, PORT))  

    def send(self, message):
        self.socket.send(message.encode())
        return(self.socket.recv().decode())

    def close(self):
        self.socket.close()