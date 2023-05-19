# From: https://github.com/VolteraInc/camera/blob/InitialCommits/volteracamera/control/camera.py
"""
Class for interfacing with the camera.
"""
import time
from io import BytesIO
from PIL import Image
import numpy as np

import importlib
picam_spec = importlib.util.find_spec("picamera")
picam_found = picam_spec is not None
if picam_found:
    from picamera import PiCamera


RESOLUTION = (1280,720)
ZOOM = (320/1920, 180/1080, 1280/1920, 720/1080)
AWB_MODE = "off"
AWB_GAINS = 1.6
FRAMERATE = 30
SHUTTER_SPEED = 5000
EXPOSURE_MODE = "off"

class Camera(object):
    """
    Class that reads from the camera.
    """

    def __init__(self):
        """
        Initialization of the camera.
        """
        if picam_found:
            print("Starting Camera")
            self.camera = PiCamera(sensor_mode = 1)
            self.camera.resolution = RESOLUTION
            self.camera.zoom = ZOOM
            self.camera.awb_mode = AWB_MODE
            self.camera.awb_gains = AWB_GAINS
            self.camera.framerate = FRAMERATE
            #time.sleep(3)
            #self.camera.shutter_speed = SHUTTER_SPEED
            #self.camera.exposure_mode = EXPOSURE_MODE


    def capture_stream(self)->BytesIO:
        """
        Return a PIL image.
        """
        stream = BytesIO()
        if picam_found:
            self.camera.capture(stream, format="jpeg", quality=65, resize = (int(RESOLUTION[0]/2), int(RESOLUTION[1]/2))) #switch to rgb later
        stream.seek(0)
        return stream
    
    def capture_image(self)->Image:
        """
        Return a PIL image.
        """
        return Image.open(self.capture_stream()) 


    def capture_array(self)->np.ndarray:
        """
        Return a 3 channel np.array (RGB)
        """
        output = np.empty((RESOLUTION[1], RESOLUTION[0], 3), dtype=np.uint8)
        if picam_found: 
            self.camera.capture(output, format="rgb")
        return output

    def open(self):
        """
        Start the camera preview
        """
        #self.camera.start_preview()
        #time.sleep(2)
     
    def __enter__(self):
        """
        Context manager enter
        """
        self.open()
        return self

    def close(self):
        """
        Called to clean up camera context.
        """
        if picam_found:
            self.camera.close()

    def __exit__(self, *args):
        """
        Context manager exit
        """
        self.close()

def preview_camera():
    """
    Method to preview the camera (requires a GUI).
    """
    import timeit
    num_images=10
    with Camera() as cam:
        start = timeit.default_timer()
        for i in range(num_images):
            print("Capturing raw image " + str(i) )
            _ = cam.capture_array()
        diff = timeit.default_timer() - start
        print ("Captured " + str(num_images) + " raw images in " + str(diff) + "s.")
        start = timeit.default_timer()
        for i in range(num_images):
            print("Capturing jpeg image " + str(i) )
            _ = cam.capture_image()
        diff = timeit.default_timer() - start
        print ("Captured " + str(num_images) + " jpeg images in " + str(diff) + "s.")   