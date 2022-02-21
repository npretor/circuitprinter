# PWM pins: 18, 12, 13, 19

import os 
import sys
import gpiozero
import time
from gpiozero import LED



class LightController:
    def __init__(self, pin='17'):
        self.pin = str(pin)
        os.system('gpio -g mode {} output'.format(pin))
        
    def on(self):
        os.system('gpio -g write {} 1'.format(self.pin))
    
    def off(self):
        os.system('gpio -g write {} 0'.format(self.pin))


if __name__ == "__main__":
    led = LightController(17)

    for i in range(1, 10):
        led.on()
        print('on')
        time.sleep(1)
        led.off()
        print('off')
        time.sleep(1) 