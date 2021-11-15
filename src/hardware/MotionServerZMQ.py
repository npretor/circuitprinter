# This motionServer should work across all devices, 
# It is the motionController classes that are device specific
# That means this is the thing that chooses the motion system
#   I should also specify settings, like speed it don't need to specified each time

import json
import time
#from crealityMotionController import MotionController
from DuetController import DuetController
import zmq
import logging



# - - - - - - - - Variables - - - - - - - - #
HOST = '*'
PORT = 5555
hardware_options = ['duet', 'shapeoko']
currentHardware = hardware_options[0]

# - - - - - - -  Hardware selection - - - - - - - - #
print(' = = = Please enter the hardware you are using = = = =')
print(' = = = = = = = = shapeoko duet = = = = = = = = = = = =')
res = input('Hardware: ')

if 'duet' in res: 
    logging.debug('Duet selected, initializing')
    currentHardware='duet'
elif 'shapeoko' in res:
    logging.debug('Shapeoko selected, initializing')
    currentHardware='shapeoko'
else:
    exit("hardware not found, exiting")

if currentHardware == 'duet':
    motion = DuetController()
    motion.connect()
    motion.home()
    time.sleep(5)
    print('motion initialized')
if currentHardware == 'shapeoko':
    logging.error('hardware not supported yet')
    sys.exit(0)


def processCommandDuet(json_packet):
    try: 
        data = json.loads(json_packet)
        print(data)
    except: 
        print('improperly formatted JSON string')
        print(json_packet)
        motion.disconnect()
        return 0

    speed = 2000

    if "moveAbs" in data:
        motion.send('G0 X{} Y{} Z{} F{}'.format(data['moveAbs'][0], data['moveAbs'][1], data['moveAbs'][2], speed))
        return {'status': 1}
    elif "moveRel" in data:
        motion.send('G91')  # set relative
        motion.send('G0 X{} Y{} Z{} F{}'.format(data['moveRel'][0], data['moveRel'][1], data['moveRel'][2], speed))
        motion.send('G90')  # set absolute
        return {'status': 1}
    elif "getPosition" in data: 
        positionString = motion.getPosition()
        locations = positionString.split()
        xPos = float(locations[0][2:])
        yPos = float(locations[1][2:])
        zPos = float(locations[2][2:])
        return {'location': {"x": xPos, "y": yPos, "z": zPos}}
    elif "close" in data:
        motion.disconnect()
        print('disconnected')
        return {'status': 1} 
    else:
        print('Error, key not found:   {}'.format(json_packet))
        return {'status': 0} 


while __name__ == '__main__':
    print('creating a socket')

    context = zmq.Context() 
    socket = context.socket(zmq.REP) 
    try:
        socket.bind("tcp://{}:{}".format(HOST, PORT))  
    except:
        print('could not connect, exiting')
        sys.exit(0)

    while True: 
        rcvdData = socket.recv().decode('utf-8') 
        if len(rcvdData) > 1:
            if currentHardware == 'duet':
                processed_result = processCommandDuet(rcvdData)
                message = json.dumps(processed_result).encode()
                socket.send(message)
            if currentHardware == 'shapoko':
                sys.exit(0)
                logging.error("hardware not supported, exited")
        else:
            print('Disconnecting...')
            socket.close()
            print('Disconnected')
            break