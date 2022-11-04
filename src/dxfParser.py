import sys
import logging 
import ezdxf

def dxf_to_list(FILENAME):
    '''
    Inputs: A dxf file. This only processes lines and polylines, and currently pulls from any layer 

    Output: array of arrays. Each array is a polyline of float tuples, no Z data
        Example of two lines: [ [(0.0,0.0), (10.0, 0.0), (10.0,10.0), (0.0, 0.0)], [(3.0, 3.0), (5.0, 5.0)] ]
    '''

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
            logging.info('Line: {} {} {} {}'.format(e.dxf.start[0], e.dxf.start[1], e.dxf.end[0], e.dxf.end[1]))
            points.append([(e.dxf.start[0], e.dxf.start[1]), (e.dxf.end[0], e.dxf.end[1])])
        elif e.dxftype() == 'LWPOLYLINE':
            poly = []
            for component in e:
                logging.info('PL component: {}'.format(component))
                poly.append( (component[0], component[1]) )
            points.append(poly)
        else: 
            logging.warning('Unknown entity type found: {}'.format(e.dxftype()))
                
    return points