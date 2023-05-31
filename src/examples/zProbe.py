"""
Z 6.05 at the bed 
Z -1.4 at the z probe location  
delta is: +7.45 
"""

import time
import sys, glob
sys.path.append('../')
from gpiozero import Button 
from hardware.MotionClientZMQ import MotionClient

offset = 7.45


probe_pin=4
probe = Button(probe_pin) 

# Connect 
serial_port = glob.glob('/dev/ttyACM*')[0] 
motion = MotionClient(serial_port=serial_port) 
print("connected: ", motion.connect(test_mode=False)) 
time.sleep(0.5)

# Home 
motion.gcode('G28')
time.sleep(10) 

# Run the unload. Grab the tool 
motion.gcode("T-1")
time.sleep(10)

motion.gcode("T2")
time.sleep(10)

motion.gcode("G1 Z15 F1500")  
time.sleep(10) 
# Probe location: (315, 152, 15) 

probe_location = [315, 152, 15]
motion.gcode("G1 X{} Y{} Z{} F1500".format(probe_location[0], probe_location[1], probe_location[2])) 
time.sleep(10)

# Send motion commands as long as a bump is not detected 
motion.gcode('G91')  # set relative moves 

print('beginning probing')

# Drop down slowly until touching 
total_distance = 0.0

while True:
    if probe.is_pressed:
        break 
    else:
        total_distance += 0.1 
        motion.gcode('G1 Z-0.10 F750')  
        time.sleep(0.2)

print('total distance: ', total_distance)

# Save and print position
position = motion.position()
print(position)

motion.gcode('G1 Z{} F500'.format(offset)) 
time.sleep(5) 

# Raise up 
motion.gcode('G1 Y3 F500')  
time.sleep(1)
motion.gcode('G1 Z10 F500')  

motion.gcode('G90')

# Save and print position
position = motion.position()
print(position)

# Unload tool 
motion.gcode("T-1") 
motion.disconnect() 