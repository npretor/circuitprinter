import sys
import os
import logging 
import ezdxf
import gerber
import gerberex
#from gerber.render.cairo_backend import GerberCairoContext
import shapely
from shapely.geometry import LineString, Point, box
from shapely.ops import cascaded_union, unary_union

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

    def gbr_to_list(self, filepath):
        """
        Inputs: 
            filepath for a .g** file. Also: .GBR, .GTL
        Outputs: 
            Shapely object. Need to move to using shapely objects alone 


        # - - - - - - - - - Import file - - - - - - - - - #
        objects = [] 
        print_layer = gerber.read(os.path.join(filepath)) 
        ctx = gerberex.GerberComposition() 

        for item in print_layer.primitives:
            if 'Line' in str(type(item)):
                # start, end, aperture, level_polarity=None            
                objects.append(LineString([(item.start[0], item.start[1]), (item.end[0], item.end[1])]).buffer(item.aperture.diameter/2))
                pass

            if 'Circle' in str(type(item)):
                # position, diameter, hole_diameter=None, hole_width=0, hole_height=0
                #print('Circle: {}'.format(item.diameter))
                objects.append(Point(item.position).buffer(item.diameter/2))
                

            if 'Polygon' in str(type(item)):  
                # position, sides, radius, hole_diameter=0, hole_width=0, hole_height=0            
                #print('Position: {} Format: {}'.format(item.position, item.sides))
                pass

            if 'Rectangle' in str(type(item)):  
                # position, width, height, hole_diameter=0, hole_width=0, hole_height=0            
                #print("Rectangle Pos: {} Width: {} Height: {}".format(item.position, item.width, item.height))
                # minx, miny, maxx, maxy
                objects.append( box(item.position[0]-(item.width/2), 
                                    item.position[1]-(item.height/2), 
                                    item.position[0]+(item.width/2), 
                                    item.position[1]+(item.height/2)
                                   ))
                                   

            #start, end, center, direction, aperture, quadrant_mode, level_polarity
            if 'Arc' in str(type(item)):
                pass

            # position, width, height
            if 'Ellipse' in str(type(item)):
                pass

            # position, width, height
            if 'Diamond' in str(type(item)): 
                pass
            if 'ChamferRectangle' in str(type(item)):              
                pass
            if 'RoundRectangle' in str(type(item)):   
                pass
            # position, width, height, hole_diameter=0, hole_width=0,hole_height=0  
            if 'Obround' in str(type(item)):  
                pass
            else: 
                print("Unknown: {}".format(item)) 
                
        
        
        """