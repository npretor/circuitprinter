"""
Questions: 
    * What is coordinate 0,0,0?

tools = [Tool1, Tool2]

Tool
    Offset
    parking_location
    
GetTool
"""

import json
import os, sys
from hardware.MotionClient import MotionClient


class Tool:
    """
    Tool
    
    """
    def __init__(self, name) -> None:
        self.name = name
        self.activeTool = None

    def load(self, toolNumber):
        
        # Run extra commands here
        try:
            # Run motion commands here     
            print('loading tool')

            return True
        except:
            return False

    def unload(self):
        return 1

class Printer:
    def __init__(self) -> None:
        self.motion = None
        self.status = 'idle'
        # states: 
        #   idle, 
        #   active
        #   error (requires restart)


    def printArtwork(self, printableCoordinates):
        for line in printableCoordinates:
            pass
        
    def startup(self):
        #  //- - - - - - - - - Load machine settings - - - - - - - - -// 
        with open('./config/machine_settings.json') as f:
            m_settings = json.load(f)

        #  //- - - - - - - - - Load ink settings - - - - - - - - -// 
        with open('./config/ink_settings.json') as f:
            ink_settings = json.load(f) 

        motion = MotionClient()

        pass

    def home(self):
        motion.send('')