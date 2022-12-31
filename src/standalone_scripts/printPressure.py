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

# Defaults:   
def printLine(startPt=(50, 10), endPt=(150, 50), printSpeed=1000, eSpeed=50, kickDst=kick, unkickDst=unkick):
    logging.info('Printing a line: {} {}'.format(startPt, endPt))
    # Move to start location at rapid speed and height
    duet.send('G0 X{} Y{} Z{} F5000'.format(startPt[0], startPt[1], m_settings['rapid_height']))

    # Drop down to print height 
    duet.send('G0 Z{} F500'.format(m_settings['tip_height']))
    
    # Print: Kick, Pause, Print line to end, Pause, Unkick
    # Kick
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

''''
Start point: 
End point  : 
'''
import sys
import ezdxf
import logging

FILENAME = 'example_artwork/Adafruit_RGBW_LED_printlayer.dxf' 
selected_ink = "ACI FE3124"
tool = 1

def dxfToPointsArray(FILENAME):
    '''
    Inputs: A dxf file. This only processes lines and polylines, and currently pulls from any layer 

    Output: array of arrays. Each array is a polyline of float tuples, no Z data
        Example of two lines: [ [(0.0,0.0), (10.0, 0.0), (10.0,10.0), (0.0, 0.0)], [(3.0, 3.0), (5.0, 5.0)] ]
    '''
    start_delay = 100       # milliseconds
    end_delay = 100       # milliseconds
    points = [] 

    # - - - - - - - - - Import file - - - - - - - - - #
    try:
        doc = ezdxf.readfile(FILENAME)
    except IOError:
        logging.warning(f'Not a DXF file or a generic I/O error.')
        sys.exit(1)
    except ezdxf.DXFStructureError:
        logging.warning(f'Invalid or corrupted DXF file.')
        sys.exit(2)

    # - - - - - - - - - Read lines and polylines - - - - - - - - - #
    msp = doc.modelspace()
    for e in msp:
        if e.dxftype() == 'LINE':
            #print('Found a line')
            logging.info('Line: {} {} {} {}'.format(e.dxf.start[0], e.dxf.start[1], e.dxf.end[0], e.dxf.end[1]))
            points.append([(e.dxf.start[0], e.dxf.start[1]), (e.dxf.end[0], e.dxf.end[1])])
        elif e.dxftype() == 'LWPOLYLINE':
            #points.append((), ())
            poly = []
            #print('Found a plyline')
            for component in e:
                logging.info('PL component: {}'.format(component))
                poly.append( (component[0], component[1]) )
            points.append(poly)
        else: 
            logging.warning('Unknown entity type found: {}'.format(e.dxftype()))
                
    return points

# Speed should be in mm/s
def printLinePressure(startPt, endPt, printSpeed=1000):
    logging.info('Printing a line: {} {}'.format(startPt, endPt))
    # Move to start location at rapid speed and height
    duet.send('G0 X{} Y{} Z{} F5000'.format(startPt[0], startPt[1], m_settings['rapid_height']))

    # Drop down to print height 
    duet.send('G0 Z{} F500'.format(m_settings['print_height']))
    
    # Pressure on
    duet.send('M106 P0 S1.0')

    # Pause (technically a dwell, units=milliseconds)
    #duet.send('G4 {}'.format(ink_settings['pause_start']))

    # Print trace 
    duet.send('G0 X{} Y{} F{}'.format(endPt[0], endPt[1], printSpeed))

    # Pause (technically a dwell, units=milliseconds)
    #duet.send('G4 {}'.format(ink_settings['pause_end']))

    # Pressure off
    duet.send('M106 P0 S0.0')

    # Raise up to rapid height
    duet.send('G0 Z{} F5000'.format(m_settings['rapid_height']) )

for polyline in polylines: 
    print('Start point{} {} {}').format(polyline[0][0], polyline[0][1], m_settings['rapid_height']) 
    #printLine(start, end, printSpeed=1000, eSpeed=50) 
    # Rapid to polygon start point 
    duet.send('G0 X{} Y{} Z{} F{}'.format(x, y, z, speed))

    # Pressure on
    #duet.send('M106 P0 S1.0')

    # Start delay

    for point in polyline[1:]: 
        print(point)


''' 
Order of operations: 

Select tool 

1. Select the print tool 
2. Print a calibration loop
3. Take photo of calibration location 

4. If artwork has a layer called fiducials AND it has entities, start calibration 
    a. Move to calibration location 1
    b. Move to calibration location 2
    3. Convert artwork to aligned artwork 
3. Print artwork



For each polyline: 
    a. Rapid to starting location on the PT0, at the rapid Z height 
    b. Drop down to the Z height 
    c. Pressure on 
        aa. Delay
            5. Move to each point at speed, skipping the first point
        bb. Delay 
    d. Pressure off 
    e. Lift up to rapid height (might need to twice to prevent trailing 
'''


duet.send('T-1') 

lights.off()
duet.disconnect() 
