# This motionServer should work across all devices, 
# It is the motionController classes that are device specific
# That means this is the thing that chooses the motion system
#   I should also specify settings, like speed it don't need to specified each time


"""
What I should do every time: 

Receive a command from the client 
Reply with the 

"""
import time
import logging
import json
import zmq
from MotionController import MotionController 

motion = MotionController(test_mode=False) 
motion.connect() 
time.sleep(2)
motion.home()
time.sleep(5)

logging.basicConfig(level=logging.INFO)

validMessages = {
    "gcode": "G0 X1 Y1", # Returns response from serial
    "getPosition": [], 
    "connect": {"port": "/dev/ttyACM0", "baudrate": 115200, "test_mode": False} ,
    "disconnect": "", 
    "home": "", 
    "getStatus": ""
}

validResponses = {
    "result" : True, 
    "status": {
        "hw_connected": True, 
    }
}


# - - - - - - - - Variables - - - - - - - - #
HOST = '*'
PORT = 5555


def processCommand(message):
    message = json.loads(message)

    if "status" in message:
        # Get status and return message 
        return {"result":True}

    elif "gcode" in message:
        # Send a generic command and return reply and status 
        res = motion.send(message['gcode']) 
        return {"result": res} 

    elif "getPosition" in message: 
        # Run and return result 
        return {"result":True} 

    elif "connect" in message: 
        """ Connect or disconnect the hardware and return status """
        motion = MotionController(message["connect"]["port"], message["connect"]["baudrate"], message["connect"]["test_mode"]) 
        if motion.connect() == True:
            return {"result": True} 
        else:
            return {"result": False} 

    else:
        logging.error("Could not parse message")


def processCommand2(incoming):
    try:
        message = json.loads(incoming) 
    except:
        logging.error("Cannot process json, exiting")
        motion.disconnect()
        return 0

    if 'gcode' in message:
        motion.send(message['gcode'])
        res = {'status': True}

    elif 'moveRel' in message:
        coords = message['moveRel']  
        motion.send('G0 X{} Y{} Z{} F{}'.format(coords[0], coords[1], coords[2], 1000))


    elif 'moveAbs' in message: 
        coords = message['moveAbs']
        motion.send('G91')
        motion.send('G0 X{} Y{} Z{} F{}'.format(coords[0], coords[1], coords[2], 1000))
        motion.send('G90')
    
    elif 'getPosition' in message:
        # parse position 
        return 0

    return res 


while __name__ == '__main__':
    logging.info('creating a socket') 

    context = zmq.Context() 
    socket = context.socket(zmq.REP) 

    try:
        socket.bind("tcp://{}:{}".format(HOST, PORT))  
    except:
        logging.error('Could not connect, exiting')
        sys.exit(0)

    while True: 
        rcvdData = socket.recv().decode('utf-8') 
        if len(rcvdData) > 1:
            processed_result = processCommand2(rcvdData)
            message = json.dumps(processed_result).encode()
            socket.send(message)

        else:
            logging.info('Disconnecting...')
            socket.close()
            logging.info('Disconnected')
            break 

finally:
    motion.close() 
    socker.close()