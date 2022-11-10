import sys
import logging 
import ezdxf

class ArtworkParser:
    def __init__(self) -> None:
        pass

    def read(self, filepath):
        if filepath.endswith('.dxf'):
            surfacePath = []
            surfacePath = self.dxf_to_list(filepath)
            return surfacePath 
        elif filepath.endswith('.gbr'):
            print("File type not supported") 
        else:
            print("Unknown file type")
            

    def dxf_to_list(self, filepath): 
        """    
        Inputs: 
            filename A dxf file. This only processes lines and polylines, and currently pulls from any layer 

        Output: array of arrays. Each array is a polyline of float tuples, no Z data
            Example of two lines: [ [(0.0,0.0), (10.0, 0.0), (10.0,10.0), (0.0, 0.0)], [(3.0, 3.0), (5.0, 5.0)] ]
        """

        # - - - - - - - - - Import file - - - - - - - - - #
        try:
            doc = ezdxf.readfile(filepath) 
        except IOError:
            logging.warning(f'Not a DXF file or a generic I/O error.')
            sys.exit(1)
        except ezdxf.DXFStructureError:
            logging.warning(f'Invalid or corrupted DXF file.')
            sys.exit(2)

        # - - - - - - - - - Read lines and polylines - - - - - - - - - #
        points = [] 
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