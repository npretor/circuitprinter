import json
from hardware.DuetController import DuetController
import logging 
"""


"""

#  = = = = = = =  Core  = = = = = = =  # 

class Printer:
    def __init__(self) -> None:
        """
        """
        self.startup()
        self.maxTools = 4

        self.stateConfig = { 
            "tools" : {
                1: {
                    "tool_name" : "Trace paste extruder",
                    "tool_type" : "paste_extrusion",
                    "tool_offsets": [0,0,0],
                },
                2: {
                    "tool_name" : "Adhesive paste extruder",
                    "tool_type" : "paste_extrusion",
                    "tool_offsets": [0,0,0], 
                },               
                3: {
                    "tool_name" : "HQ Camera",
                    "tool_type" : "camera",
                    "tool_offsets": [0,0,0]
                }
            }
        }
       
    def addTool(self, tool_name, tool_type, tool_offsets):
        """
        Returns True or false 
        """
        if self.maxTools == len(self.stateConfig["tools"]):
            print("Tools full")
            return False
        else:
            self.stateConfig["tools"][len(self.stateConfig["tools"])+1] = {
                "tool_name": tool_name,
                "tool_type": tool_type,
                "tool_offsets": tool_offsets
            }
            return True 

    def startup(self, configuration):
        """
        Order of operations
        
        """
        self.loadPreviousState(self.stateConfig)

        # Connect to hardware. In this case that's just the E3D. Later will be the camera 
        motion = DuetController() 
        try:
            motion.connect() 
        except: 
            return False
        
        # Home 
        motion.home()

        # Run machine-specific startup commands
        motion.send('M302 P1')    # Allow cold extrudes

        return True
        
    def loadPreviousState(self, stateConfigPath):
        pass

    def connectToHardware(self):
        return True

class ExtrusionProcess(Printer):
    """
    TODO: Make the process steps iterables 
    TODO: Make extrusion derivative of a higher class
    """
    def __init__(self, file_path, file_type, tool, process_settings) -> None:
        self.file_path = file_path
        self.file_type = file_type 
        self.tool = tool
        self.process_settings = process_settings
        self.motion = None

        self.ink_settings = None

    def run(self):
        surface_path = self.parseDesign(self.file_path, self.file_type) 
        machine_code = self.createMachineCode(surface_path, self.tool, self.process_settings) 
        self.runProcess(machine_code)

    def parseDesign(self, filePath, fileType):
        """
        Parse the file, return the path on a surface 
        """
        
        surfacePath = [  ]
        return surfacePath 
    
    def createMachineCode(self, surface_path, tool, process_settings, ink_settings):
        """
        Returns a list containing lines of machine code 
        """
        machine_code = []

        for line in surface_path:
            # Extrude
            motion.send('G0 E{}'.format(ink_settings['kick']))

            # Pause (technically a dwell, units=milliseconds)
            motion.send('G4 {}'.format(ink_settings['pause_start']))

            # Move to print trace 
            motion.send('G0 X{} Y{} F{}'.format( 100, 200,  200))

            # Pause (technically a dwell, units=milliseconds)
            motion.send('G4 {}'.format(ink_settings['pause_end']))

            # Retract
            motion.send('G0 E{}'.format(ink_settings['unkick']))


        return machine_code 

    def runProcess(self, machine_code):
        # Set status: ["idle", "paused", "stop"] 
        # For line in code
        return True

    def saveProcess(self):
        """
        Save the machine code, artwork, and settings
        """
        return True 
    
    def loadSettings(self):
        # Load machine settings 
        try:
            with open('./config/machine_settings.json') as f:
                self.machine_settings = json.load(f)
        except:
            logging.error('Could not load machine settings, aborting') 
            return False
        
        # Load ink settings
        try:
            with open('./config/inks.json') as f:
                self.ink_settings = json.load(f) 
        except:
            logging.error('Could not load ink settings, aborting') 
            return False
        return True



#  = = = = = = =  Tools  = = = = = = =  # 

class Project:
    def __init__(self) -> None:
        pass

class ProcessStep:
    def __init__(self) -> None:
        self.process_types = ["extrusion", "pick and place", "point cure", "bed cure"] 
        self.process_step_artwork = None
        self.toolRecipe = None

class Tool:
    def __init__(self) -> None:
        pass

class CurrentHardware:
    def __init__(self) -> None:
        pass


#  = = = = = = =  Tools  = = = = = = =  # 
class BedHeater:
    def __init__(self) -> None:
        pass

class UVCureHead:
    def __init__(self) -> None:
        pass

class FirmwareFlasher:
    def __init__(self) -> None:
        pass

class SilverExtruder:
    def __init__(self) -> None:
        pass

class PickAndPlace:
    def __init__(self) -> None:
        pass

class Camera:
    def __init__(self) -> None:
        self.available_tools = None 

