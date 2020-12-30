import os 
import sys
from gpiozero import LED

class pressureController:
    def __init__(self, pin='12'):
        device = gpiozero.DigitalOutputDevice(pin)
        return device

    def on(self):
        self.on()
    
    def off(self):
        self.off()

