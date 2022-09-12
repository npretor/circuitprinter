# Assume the motion system has been homed already

import time
import json
import ezdxf
from hardware.DuetController import DuetController
from hardware.LightController import LightController

#  //- - - - - - - - - Initialization - - - - - - - - -// 
motion = DuetController()
motion.connect()
leds = LightController()
leds.on()
time.sleep(1)

#  //- - - - - - - - - Load machine settings - - - - - - - - -// 
with open('./config/machine_settings.json') as f:
    m_settings = json.load(f)

#  //- - - - - - - - - Load ink settings - - - - - - - - -// 
with open('./config/inks.json') as f:
    ink_settings = json.load(f) 

def parsePosition(): 
    positionString = motion.get_absolute_position()
    locations = positionString.split()
    xPos = float(locations[0][2:])
    yPos = float(locations[1][2:])
    zPos = float(locations[2][2:])
    #print('Current position:  {} {} {}'.format(xPos, yPos, zPos))
    return [xPos, yPos, zPos]

def zCalibrationAuto(tool):
    # https://duet3d.dozuki.com/Wiki/Gcode#Section_M585_Probe_Tool
    # https://forum.duet3d.com/topic/8302/trying-to-understand-and-use-m585/2
    # https://forum.duet3d.com/topic/8116/setting-wcs-with-probe/4
    
    
    time.sleep(1)
    # Move to calibration location 
    xloc = m_settings['z_cal_location']['x']
    yloc = m_settings['z_cal_location']['y']
    zloc = m_settings['z_cal_location']['z']

    motion.send('G0 X{} Y{} Z{} F10000'.format(xloc, yloc, zloc)) 
    time.sleep(2)
    # We want an active low probe, so S0
    motion.send('M585 Z5 E3 L0 F100 S1')            # 

    motion.send('T{}'.format(tool))                 # Select tool 
    motion.send('G10 P{} Z0 X0 Y0'.format(tool))
    motion.send('M574 Z0 S1 P')                     # TODO: check the IO number and state . Not sure if this is active high or low
    motion.send('G0 Z10 F1000')                     # Lower bed to avoid collisions
    #motion.send('G0 X')                            # Move nozzle to avoid stuff
    motion.send('G0 X{} Y{} '.format(xloc, yloc))   # Move nozzle to cal location
    motion.send('G1 H3 Z1 F100')                    # Move type: terminate at trigger
    zloc1 = motion.parsePosition()                  # 
    #motion.resetaxislimits()                       # Reset axis limits, replace M208 in the config file
    motion.send('G0 Z1')
    motion.send('G1 H3 Z1 F10')                     # TODO: check the io number
    zloc2 = motion.parsePosition()
    motion.send('')
    #motion.resetaxislimits()
    if zloc2 < 1.1:                                 # Likely a miss
        return 0 
    motion.send('G0 Z10 F1000')                     # Lower bed to avoid collision
    motion.send('M574 Z1 S1 P{}')                   # CHECK
    return True

def zCalibrationRPI(tool): 
    motion.send('T{}'.format(tool))                 # Select tool 
    time.sleep(5)

    # Move to calibration location 
    xloc = m_settings['z_cal_location']['x'] 
    yloc = m_settings['z_cal_location']['y'] 
    zloc = m_settings['z_cal_location']['z'] 
    motion.send('G0 X{} Y{} Z{} F10000'.format(xloc, yloc, zloc)) 
    time.sleep(2)

    while probePinValue:
        # Move down 
        pass

def zCalibrationManual(tool):
    # Move to calibration location 
    xloc = m_settings['z_cal_location']['x']
    yloc = m_settings['z_cal_location']['y']
    zloc = m_settings['z_cal_location']['z']

    motion.send('G0 X{} Y{} Z{}'.format(xloc, yloc, zloc + 5))
    parsePosition

#zCalibration(0)

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


#print(parsePosition())
"""
l1_polygons = dxfToPointsArray('/home/pi/hubgit/circuitprinter/src/example_artwork/MSP430_print.dxf')
for polygon in l1_polygons:
    print(polygon)
"""

time.sleep(2)
leds.off()
motion.disconnect()