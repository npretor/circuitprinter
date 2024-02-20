# run this program on each RPi or Jetson to send a labelled image stream
import socket
import time
import imagezmq
import nanocamera as nano 

receiver_address =  'tcp://192.168.4.32:5555'

sender = imagezmq.ImageSender(connect_to=receiver_address)

jetson_name = socket.gethostname()      # send  hostname with each image
camera = nano.Camera()

time.sleep(5.0)                         # allow camera sensor to warm up

print('sending images now')
while True:                             # send images as stream until Ctrl-C
    image = camera.read() 
    sender.send_image(jetson_name, image)



