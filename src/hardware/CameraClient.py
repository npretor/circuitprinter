import time 
import threading 

import cv2 as cv
import imagezmq


class CameraClient:
    def __init__(self) -> None:
        self.thread = None 
        self.image_client = None 

    def start(self):
        self.thread = threading.Thread(target=self.listen_for_images) 
        self.thread.start()
        

    def stop(self):
        self.thread.join()
    
    def listen_for_images(self):
        image_client = imagezmq.ImageHub() 
        while True:
            print('listening')
            img_name, image = image_client.recv_image() 
            print('received image: ',img_name)
            cv.imwrite(img_name, image) 
            image_client.send_reply(b'OK') 
        










# m = MotionClient() 

# m.start_camera() 
# time.sleep(8) 
# print('camera started')

# m.save_image('image1.jpg') 
# print(m.cache_status()) 
# m.save_image("image2.jpg") 

# time.sleep(1)

# print('sending image')
# m.send_image() 
# print('sending another')
# m.send_image() 

# time.sleep(1) 

# m.stop_camera() 

