import json, time 


from hardware.MotionClientZMQ import MotionClient

m = MotionClient()
print(m.connect() )

m.send(json.dumps({'gcode': 'G28'})) 

time.sleep(15)

m.disconnect() 