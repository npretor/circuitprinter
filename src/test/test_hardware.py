import pytest 
import sys
sys.path.append('../')
from hardware import testController

motion = testController.TestController()
motion.home()

def test_testController():
    assert motion.moveRel([1,2,3], 100) == True
    assert motion.moveAbs([1,2,3], 100) == True
    
def test_homing():
    motion.home()
    assert motion.position == [0,0,0]
