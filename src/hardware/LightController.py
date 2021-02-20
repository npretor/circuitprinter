import os 
import sys
import gpiozero
from gpiozero import LED

class LightController:
    def __init__(self, pin='4'):
        self.device = gpiozero.DigitalOutputDevice(pin)
        

    def on(self):
        self.device.on()
    
    def off(self):
        self.device.off()

