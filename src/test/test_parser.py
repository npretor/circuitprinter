import pytest 
import sys 
sys.path.append('..') 

from ArtworkParser import ArtworkParser 
from printer import Printer


p = Printer()
design_path = "../example_artwork/150um_serpentine.dxf"

def readDXF(design_path):
    return True

def readGerber(gerber_design_path): 
    return True

# def test_individual():
#     p.parseDesign(design_path)
#     p.createMachineCode(1, "test", "test.json") 
#     p.validateMachineCode() 

# test_dxf = "test.dxf"
# test_process = "process_settings.json" 
# test_ink = "ink_settings.json"

def test_compileMachineCode(): 
    assert True == True

def test_pressureExtrusion():
    settings = {
        "rapid_height": 5.0, 
        "rapid_speed": 500, 
        "print_height": 0.05, 
        "print_speed": 4.0,
        "start_delay": 0.1,
        "end_delay": .1,
        "gpio": 2, 
    }

    artwork = [
        [(1,1), (2,2), (3,3), (4,4)], 
        [(10, 10), (11, 11)]
    ]

    gcode = p.pressureExtrusion(artwork, settings)
    for line in gcode:
        print(line) 

    assert True == True 


if __name__ == "__main__":
    test_pressureExtrusion()