import os 
import uuid 

from AreaSegmentation import simple_segment
"""
For each device 
    1. Get coordinates of bounding box
    2. Subdivide 



Have each step in the process be given a folder 
preprocessing 
- 
"""


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


project_name = 'test3'
root_dir = "../data"
preprocessing_steps = ['segment', 'stitch'] 


project_setup(project_name, preprocessing_steps, root_dir)

scan_devices() # Lighting, camera, and locations config 

"""
Setup 
Scan 
Stitch (if needed)
Image preprocessing
Image comparison 
"""
