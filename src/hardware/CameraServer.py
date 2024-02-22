# run this program on each RPi or Jetson to send a labelled image stream
import socket
import time
import os
import logging
import imagezmq
import nanocamera as nano 
import cv2 as cv
from collections import deque 

logging.basicConfig(level=logging.INFO) 

class CameraServer:
    """

    """
    def __init__(self, receiver_address='127.0.0.1'):
        self.receiver_address = receiver_address
        self.s = imagezmq.ImageSender(connect_to=f"tcp://{self.receiver_address}:5555" ) 

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
        
        if self.camera == None:
            print('Camera not started')
            self.start_camera()
        
        # Get image from camera 
        image = self.camera.read() 

        # Save image 
        cv.imwrite(os.path.join( "./cache_folder", image_name), image) 

        logging.info(f"Saved to cache: {image_name}")

        # Add to the cache 
        self.image_cache.append(image_name)
        

    def send_one_image(self, image_folder):
        if len(self.image_cache) > 0:
            image_path = self.image_cache.pop()

            print('image path', image_path)
            
            image = cv.imread(os.path.join('cache_folder',image_path)) 

            logging.info(f"Sending {image_path} shape: {image.shape}")

            image_name = image_path.split(os.sep)[0]

            try:
                self.s.send_image(os.path.join(image_folder, image_name), image)
            except:
                logging.error(f"Could not send image {image_folder} {image_name}")
                return False
        else:
            logging.error("Cache empty")
            return False

        return True 