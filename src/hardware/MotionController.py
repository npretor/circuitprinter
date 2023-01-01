import os 
import sys
import time
from datetime import datetime
import serial
import logging

#logging.basicConfig(filename='log_ '+ datetime.now().isoformat().replace(":", "_").replace(".","_") + '.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


def open_serial(port, baudrate):
    device = serial.Serial(port, baudrate)
    time.sleep(10)
    return device

class MotionController:
    def __init__(self, port='/dev/ttyACM0', baudrate=115200, test_mode=True):
        self.test_mode=test_mode
        self.baudrate = baudrate
        self.port = port
        self.device = None
        self.current_position = None

    def connect(self):
        if self.test_mode:
            logging.info('Connected to virtual printer') 
            return True
        else:
            try:
                self.device = open_serial(self.port, self.baudrate)
                return True
            except:
                return False
                #sys.exit(0)


    # wrapper function for connect() that prints out start banner and has delay.
    def start(self):
        self.connect()
        message = self.read()
        return message

    # Sends a message to the device and returns the response message
    def send(self, message):
        if self.test_mode:

            response="ok\n"
            return response
        else:
            message += '\r\n'
            self.device.write(message.encode('utf-8'))
            logging.info("message sent to printer: %s" % message)
            response = ''
            check = ''
            # waits to get entire message 
            while check != 'ok\n':
                check = self.device.readline().decode()
                response += check
                
            return response

    def read(self):
        response = ''
        while self.device.in_waiting > 0:
            response += self.device.readline().decode()
        return response

    def get_absolute_position(self):
        if self.test_mode:
            return self.current_position
        else:
            # get the current absolute position of print head
            return self.parsePosition(self.send('M114'))

    def parsePosition(self, line):
        res = line.split(' ') 
        logging.info("response: {}".format(res))
        
        # Only get the X, Y, and Z
        try:
            locations = [float(item[2:]) for item in res[0:3]] 
            logging.info("locations: {}".format(locations))
            return locations
        except:
            return None

    # perform homing action
    def home(self):
        if self.test_mode:
            self.current_position = [0,0,0] 
        return self.send('G28') 

    def homeXY(self):
        if self.test_mode:
            self.current_position[0] = 0.0 
            self.current_position[1] = 0.0 
        return self.send('G28 XY') 

    def setRel(self):
        return self.send("G91") 

    def setAbs(self):
        return self.send("G90")      

    def moveRel(self, coordinate, speed=1000):
        if self.test_mode:
            self.current_position[0] = float(coordinate[0]) + self.current_position[0] 
            self.current_position[1] = float(coordinate[1]) + self.current_position[1] 
            self.current_position[2] = float(coordinate[2]) + self.current_position[2] 
        self.setRel() 
        line = self.send('G0 X{}  Y{}  Z{}  F{}'.format(coordinate[0], coordinate[1], coordinate[2], speed))
        self.setAbs() 
        return line

    def moveAbs(self, coordinate, speed=1000):
        """
        TODO: calculate move time
        """
        if self.test_mode:
            self.current_position = coordinate 
        
        return self.send('G0 X{}  Y{}  Z{}  F{}'.format(coordinate[0], coordinate[1], coordinate[2], speed))
        
    def disconnect(self):
        if self.test_mode:
            logging.info("virtual motion disconnected")
            return True

        # close the serial connection
        try:
            self.device.close()
            logging.info('motion system disconnected')
            return True
        except:
            logging.info("Error closing connection.")
            return False
        time.sleep(3)
