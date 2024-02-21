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

import cv2 as cv
import imagezmq

from hardware.MotionClientZMQ import MotionClient
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
        
    def setup(self, steps, root_dir):

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
                
        return True


# project = Project('first_scan_project')
# project.setup(['segments', 'stitched'], root_dir="../data")

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

    def start_hardware(self):
        """Will need to send the ip address of the host motion system later"""
        self.motion = MotionClient(serial_port='/dev/ttyACM0', address='192.168.4.43') 

        try:
            self.motion.connect(test_mode=False) 
            logging.info("connected to motion")
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

        logging.info('starting camera')
        self.motion.start_camera()
        time.sleep(5)
        print('camera started')

        self.image_client = imagezmq.ImageHub() 

        for i, location in enumerate(self.scan_locations): 
            print("location:",location) 
            print('saving image', i)
            self.motion.save_image(f"{i}.jpg")
            time.sleep(1)

    def download_images(self, download_folder='.'):
        n_cached_images = json.loads(self.motion.cache_status())['res']
        print(n_cached_images)

        for n in range(n_cached_images):
            logging.info(f"Downloading image {n} of {n_cached_images}") 

            self.motion.send_image() 

            # Put all this into a thread 
            image_name, image = self.image_client.recv_image() 
            cv.imwrite(os.path.joint(download_folder,image_name), image) 
            self.image_hub.send_reply(b'OK') 

        
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
    # import ipdb; ipdb.set_trace()
    # Setup project 
    # If project exists, 

    myproject = Project("StitchDemo")
    myproject.setup(['segments', 'stitched'], 'data')


    
    # scanner = Scan() 
    # scanner.start_hardware()

    # print('hardware started')
    # scanner.start_scanning() 

    # scanner.download_images('./data')

    # scanner.finish() 