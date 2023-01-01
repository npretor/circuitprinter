import json
import logging
import os
from platform import machine 
from hardware.DuetController import DuetController
from ArtworkParser import ArtworkParser

class Printer:
    def __init__(self):
        self.motion = None
        self.vectorArtwork = None
        self.machineCode = None

    # = = = = = = = = Motion related functions = = = = = = = = #
    def startup(self):
        # connect to motion system
        self.connect() 
        self.home() 
        self.hardwareSpecificSetup() 
        return True
    def connect(self):
        self.motion = DuetController() 
        try:
            self.motion.connect() 
        except: 
            return False 
    def home(self):
        self.motion.home()
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #


    def hardwareSpecificSetup(self):
        # Run machine-specific startup commands
        self.motion.send('M302 P1')    # Allow cold extrudes


    def parseDesign(self, filePath):
        """ Parse the file, return the path on a surface """

        #fileType = os.path.join(filePath).split(os.sep)[-1].split('.')[-1]

        if filePath.endswith('.dxf'):
            p = ArtworkParser()
            self.vectorArtwork = p.read(filePath)
            return self.vectorArtwork 
        else:
            print("File type not supported") 

    def stepperExtrusion(self, printPaths):
        """
        Need to know: 
            Which extruder to use 

        """



        return machine_code

    def pressureExtrusion(self, polylines, settings):
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

        # 1. Select tool 
        # 2. Allow cold extrudes 

        # For each line 
        #   1. Drop down 
        #   2. Start pressure 
        #   3. Start_delay 
        #   4. Move from start to end at print height at print speed 
        #   5. Stop pressure at n units from the end 
        #   6. Raise up 
        settings = {
            "rapid_height": 5.0, 
            "rapid_speed": 500, 
            "print_height": 0.05, 
            "print_speed": 4.0,
            "start_delay": 0.1,
            "end_delay": .1,
            "gpio": 2, 
        }


        for polyline in polylines: 
            start_pt = polyline[0] 
            end_pt = polyline[:-1] 

            # Rapid to start point 
            # print("Moving to: {}".format(start_pt))
            machine_code.append('G0 X{} Y{} Z{} F{}'.format(start_pt[0], start_pt[1], settings["rapid_height"], settings["rapid_speed"])) 

            # Drop down 
            machine_code.append('G0 Z{}'.format(settings["print_height"])) 

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
        for line in self.vectorArtwork: 
            # Extrude
            machine_code.append('G0 E{}'.format(ink_settings['kick']))

            # Pause (technically a dwell, units=milliseconds)
            machine_code.append('G4 {}'.format(ink_settings['pause_start']))

            # Move to print trace 
            machine_code.append('G0 X{} Y{} F{}'.format( 100, 200,  200))

            # Pause (technically a dwell, units=milliseconds)
            machine_code.append('G4 {}'.format(ink_settings['pause_end']))

            # Retract
            machine_code.append('G0 E{}'.format(ink_settings['unkick']))

        machine_code.append('T-1')
        return machine_code 


    def validateMachineCode(self, machine_code):
        vm = self.virtualMotion()
        for line in machine_code:
            try:
                vm.send(line)
            except:
                return False
        return True 

    def saveProcess(self, gcode_list, path):
        """ 
        Save the machine code, artwork, and settings to a file
        """ 
        with open(path, 'w') as f:
            for line in gcode_list:
                f.writeline(line)  

        return True 


    def runProcess(self):
        return True 
    

    def compileMachineCode(self, filepath, process_settings, ink_settings):
        line_list = self.parseDesign(filepath)
        gcode_list = self.createMachineCode(line_list, 0, process_settings, ink_settings) 
        self.validateMachineCode(gcode_list)
        self.saveProcess(gcode_list, "./gcode/default.g") 



class Tool:
    def __init__(self, name, type, recipe, offset=[0,0,0]):
        types = set({'paste_printer', 'tool_camera', 'upward_camera', 'vacuum_tip'})
        self.offset = offset
        self.name = name
        self.type = type
        self.recipe = recipe


#paste_extruder = Tool("paste_extruder v1 homemade", "paste_extruder") 