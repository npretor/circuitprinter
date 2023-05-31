# This motionServer should work across all devices, 
# It is the motionController classes that are device specific
# That means this is the thing that chooses the motion system
#   I should also specify settings, like speed it don't need to specified each time


import time
import logging
import json
import zmq
import sys 
from MotionController import MotionController 


logging.basicConfig(level=logging.INFO)


class MotionServer:
    """
    Accepts incoming JSON strings and parses them 
    """
    def __init__(self, serial_port='/dev/ttyACM0', host='*', port='5678') -> None:
        self.serial_port = serial_port
        self.host = host
        self.port = port 
        self.test_mode = None
        self.motion = MotionController(serial_port=self.serial_port) 


    def processCommand(self, incoming):
        try:
            message = json.loads(incoming) 
        except:
            logging.error("Cannot process json") 
            return {"res": False} 

        if "gcode" in message:
            """Send a generic command and return reply and status """
            res = self.motion.send(message['gcode']) 
            return {"res": res} 

        elif "connect" in message: 
            """ Connect or disconnect the hardware and return status """
            if message['connect']:
                try:
                    logging.info('Attempting to connect to hardware')
                    self.motion.connect(message['test_mode'])
                    return {"res": True} 
                except:
                    logging.error('Could not connect to hardware over serial')
                    return {"res": False} 
            else:
                self.motion.disconnect()
                return {"res": True} 

        else:
            logging.error("Could not parse message") 
            return {"res": False} 


    def listen(self):
        logging.info('creating a socket') 

        context = zmq.Context() 
        socket = context.socket(zmq.REP) 

        try:
            socket.bind("tcp://{}:{}".format(self.host, self.port))  
        except:
            logging.error('Could not connect, exiting')
            sys.exit(0)

        while True: 
            rcvdData = socket.recv().decode('utf-8') 
            if len(rcvdData) > 1:
                processed_result = self.processCommand(rcvdData)
                message = json.dumps(processed_result).encode()
                socket.send(message) 

            else:
                logging.info('Disconnecting...')
                socket.close()
                logging.info('Disconnected')
                break 


while __name__ == '__main__':
    # Start listening, but don't connect to the motion yet 
    m = MotionServer()
    m.listen() 
