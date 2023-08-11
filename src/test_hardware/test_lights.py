import time 
import sys 
sys.path.append('..')
from hardware.LightController import LightController

side_lights = LightController(19)
 

print(side_lights.pin_type)
print(side_lights.pin)
for i in range(5):
    print('on')
    side_lights.on()
    time.sleep(1.0)

    print('off')
    side_lights.off()
    time.sleep(1.0)



print(side_lights.pin_type)
print(side_lights.pin)