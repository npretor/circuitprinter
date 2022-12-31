import pytest 
import sys 
sys.path.append('..') 

from ArtworkParser import ArtworkParser 
from printer import Printer


p = Printer()
design_path = "../example_artwork/150um_serpentine.dxf"

def readDXF(design_path):
    pass

def readGerber(gerber_design_path): 
    return True

def test_individual():
    p.parseDesign(design_path)
    p.createMachineCode(1, "test", "test.json") 
    p.validateMachineCode() 

test_dxf = "test.dxf"
test_process = "process_settings.json" 
test_ink = "ink_settings.json"

def test_compileMachineCode(test_dxf, test_process, test_ink): 
    return True