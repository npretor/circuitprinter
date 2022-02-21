# Only runs as sudo on python3
#sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
#sudo python3 -m pip install --force-reinstall adafruit-blinka

import board
import neopixel
import time


class NeopixelController:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.D18, 16, brightness=1.0)

    def on(self):
        #self.pixels.brightness = 255
        #self.pixels.fill((255,255,255))
        self.pixels.fill((255,255,255))
        self.pixels.show()
        

    def off(self):
        #self.pixels.brightness = 0
        #self.pixels.fill((0,0,0))
        self.pixels.fill((0,0,0))
        self.pixels.show()


if __name__ == "__main__":
    neopixel = NeopixelController()

    for i in range(1, 10):
        neopixel.on()
        print('on')
        time.sleep(1)
        
        neopixel.off()
        print('off')
        time.sleep(1) 
    
    neopixel.deinit()