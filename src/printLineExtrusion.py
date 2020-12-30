"""

Max speed: 0.65mm threads, 8 microsteps is 300 (mm/s? Don't know)

F is mm per minute. To get to mm per second I need to divide by 60


"""

#import logging
import time 
import json
import sys
from DuetController import DuetController


#  //- - - - - - - - - Load machine settings - - - - - - - - -// 
with open('machine_settings.json') as f:
    m_settings = json.load(f)

#  //- - - - - - - - - Load ink settings - - - - - - - - -// 
with open('ink_settings.json') as f:
    ink_settings = json.load(f)

def printLine(startPoint=(50, 10), endPoint=(150, 50)):
    # Print line: Kick, Pause, Print line to end, Pause, Unkick

    # Kick
    duet.send('G0 E{}'.format(ink_settings['kick']))

    # Pause (technically a dwell, units=milliseconds)
    duet.send('G4 {}'.format(ink_settings['pause_start']))

    # Print trace 
    duet.send('G0 X{} Y{} F{}'.format( 100, 200,  200))

    # Pause (technically a dwell, units=milliseconds)
    duet.send('G4 {}'.format(ink_settings['pause_end']))

    # Unkick
    duet.send('G0 E{}'.format(ink_settings['unkick']))


duet = DuetController()
print('created duet instance')
duet.connect()

#  //- - - - - - - - - Home - - - - - - - - -// 
#duet.home()
duet.send('M302 P1')    # Allow cold extrudes
duet.send('T2')         # Select tool 2
time.sleep(2)           # Pause  

#  //- - - - - - - - - Print a line - - - - - - - - -// 
duet.send('G0 X50 Y50 Z{} F5000'.format(m_settings['rapid_height']))

duet.send('G0 Z{} F1000'.format(m_settings['tip_height'])) # Move to a total of 100mm 
duet.send('G0 E0.55 F50')          # Prime 
duet.send('G4 100')                 # Pause

duet.send('G0 X150 Y50 F1000')      # Move 100mm

duet.send('G4 100')                 # Pause 
duet.send('G0 E-0.35 F50')         # Retract 
duet.send('G0 Z{}'.format(m_settings['rapid_height'])) 

duet.send('T-1')

duet.disconnect()


