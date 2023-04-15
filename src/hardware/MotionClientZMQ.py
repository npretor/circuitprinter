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
    def __init__(self, address='127.0.0.1', socket_port=5555):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://{}:{}".format(address, socket_port))  

    # def connect(self, port="/dev/ttyACM0", baudrate=115200, test_mode=False):
    #     message = {"connect": {"port": port, "baudrate": baudrate, "test_mode": test_mode}} 
    #     res = self.send(message)
    #     return res['result']

    # def gcode(self, message):
    #     res = self.send(message)
    #     return res['result']

    def send(self, message):
        self.socket.send(message.encode())
        return(self.socket.recv().decode())

    def close(self):
        self.socket.close()  

