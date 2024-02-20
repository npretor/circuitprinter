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

import cv2
import imagezmq


from hardware.MotionClientZMQ import MotionClient
from Configs import MatrixDeviceLayout
# from image_procesing.AreaSegmentation import simple_segment

logging.basicConfig(level=logging.INFO) 

class Project:
    def __init__(self, str: name):
        self.name = name 
        
    def setup(list: steps, str: root_dir):

        imagefolder_root_path = os.path.join(root_dir, self.name)

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


project = Project('first_scan_project')
project.setup('test3', ['segments', 'stitched'], root_dir="../data")

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
        self.image_client = None 

    def start_hardware(self, address='127.0.0.1'):
        """Will need to send the ip address of the host motion system later"""
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
        self.image_client = imagezmq.ImageHub() 

        for i, location in enumerate(self.scan_locations):            
            print(location) 
            print('saving image', i)
            self.motion.save_image(f"{i}.jpg")

    def retrieve_images():
        n_cached_images = self.motion.cache_status['cache_status']
        for n in range(n_cached_images):
            logging.info(f"Downloading image {n} of {n_cached_images}") 

            self.motion.send_image() 
            name, image = self.image_client.recv_image() 
            cv.imwrite(rpi_name, image) 
            image_hub.send_reply(b'OK') 

        
    def finish():
        """Shutdown camera and disconnect from motion controller"""
        self.motion.stop_camera() 
        self.motion.disconnect()


if __name__ == "__main__":
    """
    1. Create a workflow 
    2. Create a project 
    3. Start a scan 
    4. Download images into the project's segments folder   
        a. Have each image separated by projectName_deviceNum_segmentNum FirstScan_1_1.jpg, FirstScan_1_2.jpg
    5. Process the images 
    """
    scanner = Scan() 
    scanner.start_hardware()
    scanner.start_scanning() 
    scanner.retrieve_images()
    scanner.finish() 