import time
import sys
from gpiozero import Button 
sys.path.append('../')
from hardware.MotionController import MotionController

probe_pin=4
probe = Button(probe_pin)

# Connect 
motion = MotionController(port='/dev/ttyACM1', test_mode=False)
motion.connect()
time.sleep(1)

# Home 
motion.home()
time.sleep(10) 

# Run the unload. Grab the tool 
motion.send("T-1")
time.sleep(10)

motion.send("T2")
time.sleep(10)

motion.send("G1 Z15 F1500")  
time.sleep(10) 
# Probe location: (315, 152, 15) 

probe_location = [315, 152, 15]
motion.send("G1 X{} Y{} Z{} F1500".format(probe_location[0], probe_location[1], probe_location[2])) 
time.sleep(10)

# Send motion commands as long as a bump is not detected 
motion.send('G91')  # set relative moves 

print('beginning probing')

# Drop down slowly until touching 
total_distance = 0.0

while True:
    if probe.is_pressed:
        break 
    else:
        total_distance += 0.1 
        motion.send('G1 Z-0.10 F500')  
        time.sleep(0.1)

print('total distance: ', total_distance)

# Save and print position
position = motion.get_absolute_position()
print(position)

# Raise up 
motion.send('G1 Z3 F50') 

motion.send('G90')

# Unload tool 
motion.send("T-1") 
motion.disconnect() 