import shapely
import numpy as np

def simple_segment( 
                   bounding_box: np.ndarray, 
                   usable_camera_fov: np.ndarray, 
                   overlap = 0.1
                   ) -> list:
    """
    No rotation, segments a rectangle into cubes and returns the centers in 2D space 
    Units are in millimeters

    Inputs:
        bounding_box: tuple(float, float) (two corners, lower left and upper right) 
        subdivision_size: tuple(float, float) size in mm of the subdivisions

    """
    locations = []

    # Convert bounding_box to edges in shapely 
    non_overlap_area_x = usable_camera_fov[0] * (1-overlap) 
    print("non overlap", non_overlap_area_x) 

    return bounding_box[0] / non_overlap_area_x



"""

Get bounding box 
1. Segment 
2. 


"""

if __name__ == "__main__":
    bounding_box = np.ndarray([200,50]) 
    usable_camera_fov = np.ndarray([40,40]) 

    bounding_box = [200,50]
    usable_camera_fov = [40,40] 

    res = simple_segment(bounding_box, usable_camera_fov)
    print(res)