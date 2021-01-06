# Nathan Pretorius 2021
import sys 
import ezdxf 
import logging 



class GetDXFPolygons:
    global lines
    lines = []
    def __init__(self, path):
        self.path = path
        
        try:
            self.doc = ezdxf.readfile(self.path)
        except IOError:
            logging.warning(f'Not a DXF file or a generic I/O error.')
            sys.exit(1)
        except ezdxf.DXFStructureError:
            logging.warning(f'Invalid or corrupted DXF file.')
            sys.exit(2)
        
        self.msp = self.doc.modelspace()

        print('file imported successfully')


    def parseToArray(self):
        for e in self.msp:
            if e.dxftype() == 'LINE':
                lines.append([(e.dxf.start[0], e.dxf.start[1]), (e.dxf.end[0], e.dxf.end[1])])
            if e.dxftype() == 'LWPOLYLINE':
                poly = []
                for component in e:
                    poly.append(component[0], component[1])
                lines.append(poly)
            else:
                logging.warning('Unknown entity type found: {}'.format(e.dxftype()))
        return lines


    def parseToJSON(self):
        print('not working yet')
        pass
