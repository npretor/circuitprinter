import time 
import json
from DuetController import DuetController

# Home and level 3pt 
# Connect to tool 
# Lower bed 
# Calibrate tip Z 
# Move to rapid location
# Print line 

#  //- - - - - - - - - Load machine settings - - - - - - - - -// 
with open('machine_settings.json') as f:
    m_settings = json.load(f)

#  //- - - - - - - - - Load ink settings - - - - - - - - -// 
with open('ink_settings.json') as f:
    ink_settings = json.load(f)

        
def printLine():
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

def tool_lock():
    duet.send('G91')                   # Set relative mode
    duet.send('G1 U10 F9000 S0')         # Back off the limit switch with a small move
    duet.send('G1 U360 F9000 S1')        # Perform up to one rotation looking for the torque limit switch
    # TODO: read sensors
    duet.send('G90')                     # Set absolute mode

def tool_unlock():
    duet.send('G91')                   # Set relative mode
    duet.send('G1 U-10 F9000 S0')         # Back off the limit switch with a small move
    duet.send('G1 U-360 F9000 S1')        # Perform up to one rotation looking for the torque limit switch
    # TODO: read sensors
    duet.send('G90')                     # Set absolute mode    


duet = DuetController()
duet.connect()

#  //- - - - - - - - - Home - - - - - - - - -// 
duet.home()


#  //- - - - - - - - -  Connect to tool X - - - - - - - - -// 
duet.send('M98 P"0:/macros/tool_unlock.g"')
duet.send('G4 500')
duet.send('M98 P"0:/macros/tool_unlock.g"')
duet.send('G4 500')

duet.send('T{}'.format(m_settings['tool']))


#  //- - - - - - - - -  Adjust for probe offset - - - - - - - - -// 
#  Later we will probe for the Z height again
#  For now I'll do this manually


#  //- - - - - - - - -  Lower bed - - - - - - - - -// 
# Lower bed 
duet.send('G0 Z{}'.format(m_settings['extruder_tip_offset'])) 

#  //- - - - - - - - -  Print a line - - - - - - - - -// 


duet.disconnect()