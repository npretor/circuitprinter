"""
All units are millimeters unless otherwise specified
"""

from dataclasses import dataclass

@dataclass 
class Camera:
    """Camera settings"""
    name: str 
    exposure: float 
    shutter_speed: float 
    
    focus_distance: float 
    pixels_per_millimeter: float 
    usable_area: tuple 
 

@dataclass 
class Lights:
    """Light settings"""
    side_lights_on: bool = True 
    ring_light_on: bool = False 



class MatrixDeviceLayout:
    def __init__(self, separation, width, offset=(0.0,0.0)) -> None:
        self.offset = offset            # Offset if used
        self.separation = separation    # Center to center 
        self.width = width              # Device width 

    def generate():
        scan_locations = []
        return scan_locations


class ArbitraryLayout:
    """
    List of locations to go to
    
    """
    def __init__(self, device_centroids, transforms, offset=(0.0,0.0)) -> None:
        self.device_centroids = device_centroids        # Offset if used
        self.offset = offset                            # offset from zero 
        self.transforms = transforms                    # Not sure yet 
    
    def generate():
        scan_locations = []
        return scan_locations        