# run this program on each RPi or Jetson to send a labelled image stream
import socket
import time
import logging
import imagezmq
import nanocamera as nano 
import cv2 as cv
from collections import deque 

logging.basicConfig(level=logging.INFO) 

class CameraServer:
    """

    """
    def __init__(self, receiver_address = 'tcp://127.0.0.1:5555'):
        self.receiver_address = receiver_address
        self.s = imagezmq.ImageSender(connect_to=self.receiver_address) 

        self.image_cache = []
        self.camera = None 

    def start_camera(self):
        self.camera = nano.Camera()
        
    def stop_camera(self):
        self.camera.release()

    def start_video(self):
        self.camera = nano.Camera()

    def stop_video(self):
        self.camera.release()

    def save_image(self, image_name):
        # Get image from camera 
        image = self.camera.read() 

        # Save image 
        cv.imwrite(image_name, image) 

        logging.info(f"Saved to cache: {image_name}")

        # Add to the cache 
        self.image_cache.append(image_name)
        

    def send_one_image(self):
        if len(image_cache) > 0:
            image_path = self.image_cache.pop()
            
            logging.info(f"Sending {image_path}")

            image = cv.imread(image_path) 
            self.s.send_image(jetson_name, image)

        return True 