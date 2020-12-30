from DuetController import DuetController

d = DuetController()
d.connect()

d.send('G28')
d.disconnect()