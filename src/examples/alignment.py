import os, sys, json, time
import hardware
from hardware.MotionClientZMQ import MotionClient


# fiducial locations 

# Connect to motion 
motion = MotionClient()
motion.connect(test_mode=False)

# Move to the first location 

# Save location
# Move to the second location 
# Save location

# Set new first point as the origin 
# Use the second point to calculate the rotation 

