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
import uuid 

from hardware.MotionClientZMQ import MotionClient
from AreaSegmentation import simple_segment

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


class Scan:
    def __init__(self, MatrixDeviceLayout, CameraConfig, LightConfig):
        self.camera_config = CameraConfig
        self.light_config = LightConfig
        self.scan_locations = MatrixDeviceLayout.mock_generate() 
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

        camera_z_location  = focuz_z_locationx 

        logging.info("Initializing")
        # motion.gcode(f"G1 X{} Y{} Z{} F5000 ") 
        time.sleep(10)

        for i, location in enumerate(self.scan_locations):            
            print(location) 
            print('saving image', i)
            camera_client.save_image(f"{i}.jpg")

        self.camera.close() 
        self.motion.close() 