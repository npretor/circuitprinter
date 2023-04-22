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
    def __init__(self, port='/dev/ttyACM0', address='127.0.0.1', socket_port=5678):
        self.port = port 
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://{}:{}".format(address, socket_port))  

    def send(self, message):
        self.socket.send(message.encode())
        return(self.socket.recv().decode())
    
    def connect(self):
        return self.send(json.dumps({'connect': True}) )

    def disconnect(self):
        return self.send(json.dumps({'connect': False}) )

    def close(self):
        self.socket.close()  

