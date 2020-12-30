
# Nathan Pretorius 2020
"""
For pressure extrusion the order of operations for printing is: 
    Rapid to location
    Drop down to Z
    Pressure on
    Pause 
    Move to line end 
    Pressure off 
    Pause 
    Lift up Z 

    May have to impliment a timing method where the extrusion is stopped before the end of the print: 
    Calculate distance, and at (distance - retraction time) stop the extrusion but keep moving
    Time and pressure factor into the extrusion, for now just time
    Use speed to determine the time before the end to stop 

"""

#import logging
import time 
import json
import sys
from DuetController import DuetController
import gpiozero


#  //- - - - - - - - - Load machine settings - - - - - - - - -// 
with open('machine_settings.json') as f:
    m_settings = json.load(f)

#  //- - - - - - - - - Load ink settings - - - - - - - - -// 
with open('ink_settings.json') as f:
    ink_settings = json.load(f)

def printLine(startPoint=(50, 10), endPoint=(150, 50)):
    # Print line: Kick, Pause, Print line to end, Pause, Unkick

    # Kick
    pressure.on()

    # Pause (technically a dwell, units=milliseconds)
    duet.send('G4 {}'.format(ink_settings['pause_start']))

    # Print trace 
    duet.send('G0 X{} Y{} F{}'.format( 100, 200,  200))

    # Unkick
    pressure.off()

    # Pause (technically a dwell, units=milliseconds)
    duet.send('G4 {}'.format(ink_settings['pause_end']))


#  //- - - - - - - - - Connect to hardware - - - - - - - - -// 
duet = DuetController()
duet.connect()
print('connected to duet')

pressure = gpiozero.DigitalOutputDevice(m_settings['pressure_pin'])
print('connected to pressure on pin: {}'.format(m_settings['pressure_pin']))

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


