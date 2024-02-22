import time 
import threading 
import subprocess 

import cv2 as cv
import imagezmq


class CameraClient:
    def __init__(self) -> None:
        self.thread = None 
        self.image_client = None 
    
    def listen_for_images(self):
        self.image_client = imagezmq.ImageHub() 
        while True:
            print('listening')
            img_name, image = self.image_client.recv_image() 
            self.image_client.send_reply(b'OK') 
            print('received image: ',img_name)
            cv.imwrite(img_name, image) 


if __name__ == "__main__":
    try:
        c = CameraClient()
        c.listen_for_images()
    finally:
        c.image_client.close()