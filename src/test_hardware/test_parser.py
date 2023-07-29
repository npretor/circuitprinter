"""


"""

import sys, os  
sys.path.append('..')
import logging 
from Printer import Printer
from hardware.MotionClientZMQ import MotionClient


logging.basicConfig(level=logging.INFO)

motion = MotionClient() 
printer = Printer() 

# 1. Get the artwork 
design_path = os.path.join('../examples/artwork', 'test_serpentine.dxf') 

# 2. Parse the design 
surfacePath = printer.parseDesign(design_path) 

# 3. Zero the printer 

# 4. Apply settings 
polylines = [
    [(0,0), (10, 0), (10, 10), (0, 10), (0, 0)],
    [(0,0), (9, 0), (9, 9), (0, 9), (0, 0)]
]
tip_zero_height = 5.0 
settings = {
    "rapid_height": 5.0, 
    "rapid_speed": 1000, 
    "print_height": 1.0, 
    "z_calibration": tip_zero_height,
    "print_speed": 100.0,
    "start_delay": 0.1,
    "end_delay": .1,
    "gpio": 2, 
}

# Tool, ink_recipe, process_recipe 
printer.machineCode = printer.compilePressureExtrude(polylines, settings) 

# 5. Print 
for line in printer.machineCode:
    # motion.gcode(line)   
    print(line) 