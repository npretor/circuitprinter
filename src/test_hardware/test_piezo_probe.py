import time 
import sys 
sys.path.append('..')



import Printer 
printer = Printer.Printer() 
printer.connect() 

time.sleep(5)

# Probe the z zero 
printer.piezoProbe(2)

print("Moving to print height and location") 

# All bed locations should be zero relative to the camera for registration purposes. 
# All tools should also be registered relative to the downward camera 

printer.disconnect() 