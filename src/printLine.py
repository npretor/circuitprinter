import time 
import json
from DuetController import DuetController


#  //- - - - - - - - - Load machine settings - - - - - - - - -// 
with open('machine_settings.json') as f:
    m_settings = json.load(f)

#  //- - - - - - - - - Load ink settings - - - - - - - - -// 
with open('ink_settings.json') as f:
    ink_settings = json.load(f)

duet = DuetController()
duet.connect()

#  //- - - - - - - - - Home - - - - - - - - -// 
duet.home()

duet.send('T0')
time.sleep(5)
duet.send('T-1')

duet.disconnect()