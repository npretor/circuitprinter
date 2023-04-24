import json
import logging
import os
import time 
from platform import machine 
#from hardware.MotionController import MotionController
from hardware.MotionClientZMQ import MotionClient
from ArtworkParser import ArtworkParser
import gpiozero 
from gpiozero import Button 

class Printer:
    def __init__(self):
        self.motion = None
        self.vectorArtwork = None
        self.machineCode = None
        self.current_job = None
        self.currentToolNum = None

        self.probe_pin=4
        probe = Button(self.probe_pin) 

        self.process_recipes = None
        self.machine_settings = None 

        with open('../config/process_recipes.json','r') as f:
            self.process_recipes = json.load(f) 
            
        with open('../config/machine_settings.json','r') as f:
            self.machine_settings = json.load(f) 
        
        self.toolConfigs = {
            'tools': {
                '0': {
                    'abs_pizeo_z': 0.0 
                }, 
                '1': {
                    'abs_pizeo_z': 0.0 
                }, 
                '2': {
                    'abs_pizeo_z': 0.0 
                }, 
                '3': {
                    'abs_pizeo_z': 0.0 
                }                
            },
            'tool_to_bed_offset': 4.3 
        }            

    # = = = = = = = = Motion related functions = = = = = = = = #
    def startup(self):
        # connect to motion system
        # self.connect() 
        # self.home() 
        # self.hardwareSpecificSetup() 
        return True

    def connect(self):
        #self.motion = MotionController() 
        self.motion = MotionClient() 
        try:
            self.motion.connect() 
        except: 
            return False 

    def piezoProbe(self, toolnum=2):
        """

        """
        # Connect to an input 

        # Move to a probe location 

        # Drop the head down slowly until contact 
        self.motion.home()
        time.sleep(10)    
        # Run the unload. Grab the tool 
        self.motion.send("T-1")
        time.sleep(10)

        self.motion.send("T2")
        time.sleep(10)             
        self.motion.send("G1 Z15 F1500")  
        time.sleep(10) 
        # Probe location: (315, 152, 15)         
        probe_location = [315, 152, 15]
        self.motion.send("G1 X{} Y{} Z{} F1500".format(probe_location[0], probe_location[1], probe_location[2])) 
        time.sleep(10)

        # Send motion commands as long as a bump is not detected 
        self.motion.send('G91')  # set relative moves         

        while True:
            if self.probe.is_pressed:
                break 
            else:
                self.motion.send('G1 Z-0.10 F500')  
                time.sleep(0.1)
        
        # Save and print position
        position = self.motion.get_absolute_position()
        print(position)                
        # Save and print position
        position = self.motion.get_absolute_position()
        print(position)

        # Raise up 
        self.motion.send('G1 Z3 F50') 

        self.motion.send('G90')

        # Unload tool 
        self.motion.send("T-1")         

    def hardwareSpecificSetup(self):
        # Run machine-specific startup commands
        self.motion.send('M302 P1')    # Allow cold extrudes

    # = = = = = = = = = = Process artwork and print = = = = = = = = = # 
    def parseDesign(self, filePath):
        """ Parse the file, return the path on a surface """

        #fileType = os.path.join(filePath).split(os.sep)[-1].split('.')[-1]

        if filePath.endswith('.dxf'):
            p = ArtworkParser()
            self.vectorArtwork = p.read(filePath)
            return self.vectorArtwork 
        else:
            print("File type not supported") 
    def compileStepperExtrude(self, polylines, settings):
        """
        Need to know: 
            Which extruder to use 

        """
        return True

    def compilePressureExtrude(self, polylines, settings):
        """
        Need to know: 
            Which gpio to switch 
            Which tool to select 
            Z zeroed height 
            Print height 
            Speed 
            Start delay
            Stop delay 
            Retract height 


        """
        machine_code = []

        # Already setup
        #   1. Select tool 
        #   2. Allow cold extrudes 

        # For each line 
        #   1. Drop down 
        #   2. Start pressure 
        #   3. Start_delay 
        #   4. Move from start to end at print height at print speed 
        #   5. Stop pressure at n units from the end 
        #   6. Raise up 


        for polyline in polylines: 
            start_pt = polyline[0] 
            end_pt = polyline[:-1] 

            # Rapid to start point 
            # print("Moving to: {}".format(start_pt)) 
            machine_code.append('G0 X{} Y{} Z{} F{}'.format(start_pt[0], start_pt[1], settings["rapid_height"], settings["rapid_speed"])) 

            print_z_height = float(settings["print_height"]) + float(settings["z_calibration"])
            # Drop down 
            machine_code.append('G0 Z{}'.format(print_z_height)) 

            # Pause before start
            machine_code.append('G4 {}'.format(settings['start_delay'])) 

            # Pressure on  
            machine_code.append('M106 P{} S1.0'.format(settings['gpio']))

            for line_segment in polyline[1:]:
                # Print all but the last one 
                
                # Move 
                # print("Moving to: {}".format(line_segment)) 
                machine_code.append('G1 X{} Y{} F{}'.format(line_segment[0], line_segment[1], settings["print_speed"])) 

            # Pause (technically a dwell, units=milliseconds)
            machine_code.append('G4 {}'.format(settings['end_delay'])) 

            # Pressure off 
            machine_code.append('M106 P{} S0.0'.format(settings['gpio'])) 

            # Raise up 
            machine_code.append('G0 Z{}'.format(settings["rapid_height"])) 

        return machine_code       

    def createMachineCode(self, tool_number, process_recipe, ink_settings):
        """
        Returns a list of strings which are lines of machine code 
        """
        machine_code = []
        machine_code.append('T{}'.format(tool_number))

        machine_code.append('T-1')
        return machine_code 

    def saveProcess(self, gcode_list, path):
        """ 
        Save the machine code, artwork, and settings to a file
        """ 
        with open(path, 'w') as f:
            for line in gcode_list:
                f.writeline(line)  

        return True 

    def runProcess(self, gcode_path, tool_number, z_calibration=False):
        """
        
        Are we doing calibration? Yes/No 

        """
        # Get the tool
        self.motion.send('T{}'.format(tool_number))

        if z_calibration == True:
            # TODO: Calibrate: 
            # TODO: Apply z calibration, or set as zero point 
            pass

        else:
            pass


        
        return True 
    
    def compileMachineCode(self, filepath, process_settings, ink_settings):
        line_list = self.parseDesign(filepath)
        gcode_list = self.createMachineCode(line_list, 0, process_settings, ink_settings) 
        self.validateMachineCode(gcode_list)
        self.saveProcess(gcode_list, "./gcode/default.g") 


class Tool:
    def __init__(self, name, tool_type, recipe, offset=[0,0,0]):
        types = set({'paste_printer', 'tool_camera', 'upward_camera', 'vacuum_tip'})
        self.offset = offset
        self.name = name
        self.tool_type = tool_type
        self.recipe = recipe


#paste_extruder = Tool("paste_extruder v1 homemade", "paste_extruder") 