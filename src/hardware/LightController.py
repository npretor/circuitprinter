# PWM pins: 18, 12, 13, 19
# Using -g sets broadcom pin numbering, this is used by default

import os 
import sys
#import gpiozero
import time
#from gpiozero import LED


class LightController:
    def __init__(self, pin='17'):
        #self.pwm_pins = {12,13,18,19}
        self.pwm_pins = {12,13} #PWM pin controls are broken
        self.pin = str(pin) 
        self.pin_type = 'digital'
        
        if pin in self.pwm_pins:
            self.pin_type = 'pwm'
            os.system('gpio -g mode {} ALT0'.format(pin))
        else:
            os.system('gpio -g mode {} output'.format(pin))
        
    def on(self):
        if self.pin_type == 'pwm':
            os.system('gpio -g pwm {} 512'.format(self.pin))
        else:
            os.system('gpio -g write {} 1'.format(self.pin))

    def off(self):
        if self.pin_type == 'pwm':
            os.system('gpio -g pwm {} 0'.format(self.pin))
        else:
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