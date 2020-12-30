import serial
import time

s = serial.Serial('/dev/ttyACM0', 115200)
print(s.name)

time.sleep(1)

s.write(b'G28\r\n')
s.close()