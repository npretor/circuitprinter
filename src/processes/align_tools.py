import json
import sys
sys.path.append('../')
from hardware.DuetController import DuetController

# - - - - - - - Import settings - - - - - - - #
with open('/home/pi/hubgit/circuitprinter/src/config/machine_settings.json') as f:
    data = json.load(f)
    #print(data)
    for tool in data['tools']:
        print(tool)


# - - - - - - - Initialize hardware - - - - - - - #
motion = DuetController()
motion.connect()

# - - - - - - - Get position - - - - - - - #
positionString = motion.get_absolute_position()
print(positionString)
#motion.home()
locations = positionString.split()
xPos = float(locations[0][2:])
yPos = float(locations[1][2:])
zPos = float(locations[2][2:])
print('Current position:  {} {} {}'.format(xPos, yPos, zPos))


# - - - - - - - Calibrate  - - - - - - - #

# Start camera 
# Move to location


motion.disconnect()