import time
import picamera

camera = picamera.PiCamera()
try:
    camera.start_preview()
    time.sleep(30)
    camera.stop_preview()
finally:
    camera.close()