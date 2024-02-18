"""
For each device 
    1. Get coordinates of bounding box
    2. Subdivide 

"""
"""
Setup 
Scan 
Stitch (if needed)
Image preprocessing
Image comparison 
"""

import os 
import time 
import uuid 
import logging 

from hardware.MotionClientZMQ import MotionClient
from Configs import MatrixDeviceLayout
# from image_procesing.AreaSegmentation import simple_segment

logging.basicConfig(level=logging.INFO) 


def project_setup(name, steps, root_dir):

    imagefolder_root_path = os.path.join(root_dir, name)

    try:
        os.mkdir(imagefolder_root_path) 
    except:
        return False

    for i, step_name in enumerate(steps):

        workflow_step_folder = os.path.join(imagefolder_root_path, str(i)+'_'+step_name)

        try:
            os.mkdir(workflow_step_folder) 
        except:
            print('error creating:',workflow_step_folder)
            return False
    
    return True

project_setup('test3', ['segment', 'stitch'], "../data")

m_layout = MatrixDeviceLayout(2,2)

class Scan:
    # def __init__(self, MatrixDeviceLayout, CameraConfig, LightConfig):
    #     self.camera_config = CameraConfig
    #     self.light_config = LightConfig
    #     self.scan_locations = MatrixDeviceLayout.mock_generate() 
    #     self.motion = None 

    def __init__(self):
        self.scan_locations = m_layout.mock_generate() 
        self.motion = None 

    def start_hardware(self, address='127.0.0.1'):
        self.motion = MotionClient() 
        try:
            self.motion.connect(test_mode=False) 
            return True 
        except: 
            return False 

    def start_scanning(self):
        """

        """
        focuz_z_locationx = 100
        camera_z_location = focuz_z_locationx 

        logging.info("Initializing")
        # motion.gcode(f"G1 X{} Y{} Z{} F5000 ") 

        self.motion.start_camera()
        time.sleep(5)

        for i, location in enumerate(self.scan_locations):            
            print(location) 
            print('saving image', i)
            self.motion.save_image(f"{i}.jpg")

        self.motion.disconnect() 

if __name__ == "__main__":
    scanner = Scan() 
    scanner.start_hardware()
    scanner.start_scanning() 