import os 
import sys
import time
import serial

def open_serial(port, baudrate):
    device = serial.Serial(port, baudrate)
    time.sleep(10)
    return device

class TestController:
    def __init__(self, port='/dev/ttyACM0', baudrate=115200):
        self.baudrate = baudrate
        self.port = port
        self.device = None
        self.position = None

    def connect(self):
        try:
            #self.device = open_serial(self.port, self.baudrate)
            print('connected to test printer')
        except:
            print("Error connecting.")
            sys.exit(0) 

    def disconnect(self):
        # close the serial connection
        try:
            #self.device.close()
            print('disconnected')
        except:
            print("Error closing connection.")
            return 0
        time.sleep(3)

    def start(self):
        """wrapper function for connect() that prints out start banner and has delay."""
        self.connect()
        message = self.read()
        return message

    def send(self, message):
        """Sends a message to the device and returns the response message"""
        message += '\r\n'
        #self.device.write(message.encode('utf-8'))
        print("message sent to printer: %s" % message)
        response = ''
        check = ''
        # waits to get entire message 
        # while check != 'ok\n':
        #     check = self.device.readline().decode()
        #     response += check
            
        return response

    def read(self):
        response = ''
        while self.device.in_waiting > 0:
            response += self.device.readline().decode()
        return response

    def get_absolute_position(self):
        # get the current absolute position of print head
        #line = self.send('M114')
        line = self.position
        return line

    def home(self):
        #line = self.send('G28')
        time.sleep(5)
        self.position = [0,0,0] 
        return True

    def homeXY(self):
        #line = self.send('G28 XY')
        self.position[0] = 0.0
        self.position[1] = 0.0
        return True

    def moveRel(self, direction, speed=1000):
        """ 
        Input:
            direction: [x, y, z] 
            speed: default is 2000    
        Returns true
        """        
        #response = self.send("G0 X{} Y{} Z{} F{}".format(direction[0], direction[1], direction[2], speed))
        self.position = [self.position[0] + direction[0], self.position[1] + direction[1], self.position[2] + direction[2]] 
        return True

    def moveAbs(self, direction, speed=1000):
        """ 
        Input:
            direction: [x, y, z] 
            speed: default is 2000    
        Returns true
        """
        self.position = direction 
        return True 