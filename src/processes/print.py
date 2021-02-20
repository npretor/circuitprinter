
test_lines = [
    [(0,0), (10,0), (10,10), (0,10), (0,0)], 
    [(0,0), (10,10)]
    ]

def calibrate():
    # Get correct tool 
    # 

def printArtwork(polylines):
    """
    Print line from an array: 
    [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]

    """
    for line in polylines: 

        # rapid to startPoint
        duet.send('G0 X50 Y50 Z{} F5000'.format(m_settings['rapid_height']))
        
        # Drop down to zero 
        duet.send('G0 X{} Y{} Z{} F{}'.format(x, y, z, print_speed))

        for point in line: 
