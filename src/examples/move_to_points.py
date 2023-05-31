import os, sys, json, time
import hardware
from hardware.MotionClientZMQ import MotionClient


# def test_connection():
#     """
#     1. Startup the motion server 
#     2. Init the motion client 
#     3. Tell the motion client to connect 
#     4. Verify the motion client 
#         a. Is connected
#         b. Sends back a reply  
#     """

#     os.system("cd hardware && python3 MotionServerZMQ.py") 

# test_connection() 


motion = MotionClient()
motion.connect(test_mode=False)


points = [(5, 100), (100,100), (100,5), (5,5)]

for point in points:
    motion.gcode('G0 X{} Y{} F50000'.format(point[0], point[1]) )

motion.close()