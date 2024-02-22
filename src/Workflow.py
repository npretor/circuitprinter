"""
For each device 
    1. Get coordinates of bounding box
    2. Subdivide 

Setup 
Scan 
Stitch (if needed)
Image preprocessing
Image comparison 
"""
import os 
import time 
import json 
import uuid 
import logging 
import glob
import subprocess

import cv2 as cv
import imagezmq

from hardware.MotionClientZMQ import MotionClient
# from hardware.CameraClient import CameraClient
from Configs import MatrixDeviceLayout
# from image_procesing.AreaSegmentation import simple_segment


logging.basicConfig(level=logging.INFO) 


class Project:
    """
    Projects have the following structures: 
    Projectname
        WorkflowRun_1   
            1_StepName
            2_StepName
            3_StepName
    """
    def __init__(self, name):
        self.name = name 
        
    def setup(self, steps, root_dir='./data'):

        # Root folder ./ProjectName
        project_root_path = os.path.join(root_dir, self.name)
        if not os.path.exists(project_root_path):
            try:
                os.mkdir(project_root_path) 
            except:
                logging.error("Could not make root image folder")

        # WorkflowFolder_{n}
        workflow_folders = glob.glob(os.path.join(project_root_path, 'WorkflowRun_*'))
        if len(workflow_folders) == 0:
            # Create a folder 
            os.mkdir(os.path.join(project_root_path, 'WorkflowRun_1')) 
            workflow_folder = "WorkflowRun_1"
        else: 
            # Sort the folders, get the one with the highest number
            # Get the number
            workflow_number = int(sorted(workflow_folders)[-1].split(os.sep)[-1].split('_')[-1]) 

            # Create a folder with WorkflowFolder_{n+1}
            workflow_number+=1

            workflow_folder =  f"WorkflowRun_{workflow_number}"
            os.mkdir(os.path.join(project_root_path, workflow_folder)) 

        # Create 
        for i, step_name in enumerate(steps):

            workflow_step_folder = os.path.join(project_root_path, workflow_folder, str(i)+'_'+step_name)

            try:
                os.mkdir(workflow_step_folder) 
            except:
                print('error creating:',workflow_step_folder)
    
        # Return the current workflow location 
        return os.path.join(project_root_path, workflow_folder) 


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
        self.camera_process = None 
        

    def start_hardware(self):
        """Will need to send the ip address of the host motion system later"""
        # Address is the address of the jetson
        self.motion = MotionClient(serial_port='/dev/ttyACM0', address='192.168.4.43') 
        
        # Start the image server 
        self.camera_process = subprocess.Popen(['python3', './hardware/CameraClient.py'], stdout=subprocess.PIPE) 

        time.sleep(5)
        print('camera client started')
        try:
            self.motion.connect(test_mode=False) 
            logging.info("connected to motion")
            return True 
        except: 
            return False 

    def start_scanning(self, image_folder):
        """

        """
        focuz_z_locationx = 100
        camera_z_location = focuz_z_locationx 

        logging.info("Initializing")
        # motion.gcode(f"G1 X{} Y{} Z{} F5000 ") 

        logging.info('starting camera')
        self.motion.start_camera()
        time.sleep(5)
        print('camera started')

        for i, location in enumerate(self.scan_locations): 
            print("location:",location) 
            print('saving image', i)
            self.motion.save_image(f"{i}.jpg") 
            time.sleep(1)

    def download_images(self, download_folder):
        n_cached_images = json.loads(self.motion.cache_status())['res']
        print(f"{n_cached_images} cached images")

        for n in range(n_cached_images):

            logging.info(f"Downloading image {n} of {n_cached_images}") 
            # self.motion.image_save_folder = download_folder
            self.motion.send_image(download_folder) 

            # Put all this into a thread 
            # image_name, image = self.image_client.recv_image() 
            # cv.imwrite(os.path.joint(download_folder,image_name), image) 
            # self.image_hub.send_reply(b'OK') 

        time.sleep(1)
        self.camera_process.terminate()


    def finish(self):
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

    # Setup project 
    myproject = Project("StitchDemo")
    steps = ['segments', 'stitched']
    workflow_folder = myproject.setup(['segments', 'stitched']) 

    # Start scanning 
    scanner = Scan() 
    scanner.start_hardware()
    print('hardware started')
    scanner.start_scanning(os.path.join(workflow_folder, "0_segments")) 

    stitch_folder = os.path.join(workflow_folder, steps[0])

    # cam = CameraClient()
    # cam.start()

    scanner.download_images(os.path.join(workflow_folder, "0_segments")) 
    scanner.finish() 
    # cam.stop()