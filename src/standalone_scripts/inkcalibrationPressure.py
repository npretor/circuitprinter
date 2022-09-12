"""
Nathan Pretorius 2020
Max extruder speed: 0.65mm threads, 8 microsteps is 300 (mm/s? Don't know)
Syringe diameter is 12.5mm 
Moving a total of 1mm forces a move of 

"""

import time
import json
from devices.DuetController import DuetController
import logging
import gpiozero

logging.basicConfig(level=logging.DEBUG)

#  //- - - - - - - - - Load machine settings - - - - - - - - -// 
with open('./config/machine_settings.json') as f:
    m_settings = json.load(f)

#  //- - - - - - - - - Load ink settings - - - - - - - - -// 
with open('./config/inks.json') as f:
    ink_settings = json.load(f)



duet = DuetController()
print('created duet instance')
duet.connect()
kick = 0.1
unkick = 0.1

lights = gpiozero.DigitalOutputDevice(m_settings['light_pin'])
lights.on()

def printLine(startPt=(50, 10), endPt=(150, 50), printSpeed=1000, eSpeed=50, kickDst=kick, unkickDst=unkick):
    logging.info('Printing a line: {} {}'.format(startPt, endPt))
    # Move to start location at rapid speed and height
    duet.send('G0 X{} Y{} Z{} F5000'.format(startPt[0], startPt[1], m_settings['rapid_height']))

    # Drop down to print height 
    duet.send('G0 Z{} F500'.format(m_settings['tip_height']))
    
    # Print: Kick, Pause, Print line to end, Pause, Unkick
    # Pressure on
    duet.send('M106 P0 S1.0')

    # Pause (technically a dwell, units=milliseconds)
    # duet.send('G4 {}'.format(ink_settings['pause_start']))

    # Print trace 
    duet.send('G0 X{} Y{} F{}'.format(endPt[0], endPt[1], printSpeed))

    # Pause (technically a dwell, units=milliseconds)
    #duet.send('G4 {}'.format(ink_settings['pause_end']))

    # Pressure off
    duet.send('M106 P0 S0.0')

    # Raise up to rapid height
    duet.send('G0 Z{} F5000'.format(m_settings['rapid_height']) )

#  //- - - - - - - - - Load ink settings - - - - - - - - -// 
duet.send('M302 P1')    # Allow cold extrudes
duet.send('T1')         # Select tool 2
time.sleep(2)           # Pause  

#Start locations on the sheet: from 50,50 to 200, 200
# Move from 50 to 200 in 10mm increments 

start = 50
separation = 20
end = 150

for ycoord in range(start, end, separation):
    start = (50, ycoord)
    end = (100, ycoord)
    printLine(start, end, printSpeed=1000, eSpeed=50) 
        
duet.send('T-1') 

lights.off()
duet.disconnect() 
