import os 
import sys
import time
import serial

def open_serial(port, baudrate):
    device = serial.Serial(port, baudrate)
    time.sleep(10)
    return device

class DuetController:
    def __init__(self, port='/dev/ttyACM0', baudrate=115200):
        self.baudrate = baudrate
        self.port = port
        self.device = None

    def connect(self):
        try:
            self.device = open_serial(self.port, self.baudrate)
            print('connected to printer')
        except:
            print("Error connecting.")
            sys.exit(0)

    # wrapper function for connect() that prints out start banner and has delay.
    def start(self):
        self.connect()
        message = self.read()
        return message

    # Sends a message to the device and returns the response message
    def send(self, message):
        message += '\r\n'
        self.device.write(message.encode('utf-8'))
        print("message sent to printer: %s" % message)
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
        # get the current absolute position of print head
        line = self.send('M114')
        return line

    def parsePosition(self, line):
        res = line.split(' ') 
        locations = [float(item[2:]) for item in res] 
        print("locations: ", locations)
        return locations

    # perform homing action
    def home(self):
        line = self.send('G28')
        return line

    def homeXY(self):
        line = self.send('G28 XY')
        return line

    def setRel(self):
        line = self.send("G91")

    def setAbs(self):
        line = self.send("G90")        

    def moveRel(self, direction, speed=1000):
        self.setRel()
        line = self.send('G0 X{}  Y{}  Z{}  F{}'.format(direction[0], direction[1], direction[2], speed))
        self.setAbs()
        return line

    def disconnect(self):
        # close the serial connection
        try:
            self.device.close()
            print('disconnected')
        except:
            print("Error closing connection.")
            return 0
        time.sleep(3)
