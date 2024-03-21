"""
### Jetson GPIO on/off slow switching control 

* Installation 
sudo python3 -m pip install Jetson.GPIO 

* Permissions 
sudo groupadd -f -r gpio
sudo usermod -a -G gpio your_user_name
sudo cp venv/lib/pythonNN/site-packages/Jetson/GPIO/99-gpio.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
"""

import Jetson.GPIO as GPIO

class PinController:
    def __init__(self, pin):
        self.pin = int(pin) 
        GPIO.setmode(GPIO.BCM) # This matches the labels on the RPI breakout 
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW) 
        self.state = 0 # GPIO.LOW

    def on(self):
        GPIO.output(self.pin, 1)
        self.state = 1

    def off(self):
        GPIO.output(self.pin, 0) 
        self.state = 0

    # def toggle(self):
    #     self.state=0 if self.state == 1 else self.state=1
    #     GPIO.output(self.pin, self.state)

    def close(self):
        GPIO.cleanup()