import pytest 
import sys 
sys.path.append('..')

def test_import():
    from hardware import MotionClientZMQ 
    from hardware import MotionServerZMQ 
    assert MotionServerZMQ is not None
    assert MotionClientZMQ is not None

def test_connection():
    assert True