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