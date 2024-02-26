import os 
import glob
import numpy as np
import cv2 as cv 
import matplotlib.pyplot as plt
from imutils import opencv2matplotlib

"""
1. Open artwork 
2. Open image 
3. Preprocess image 
4. Align 
5. Contrast 
"""

parameters = {
    "blob": {

    },
    "threshold":128,
}



def open_template(template_file):
    template = cv.imread(template_file, cv.COLOR_BGR2GRAY) 
    # print(template.shape)
    # gs_imagem = cv2.cvtColor(image, )
    
    return template

def open_image(image_file):
    return cv.imread(image_file, cv.IMREAD_GRAYSCALE) 

def threshold(image):
    # image  = cv.threshold(image, 128, )
    ret, thresholded = cv.threshold(image, 127, 255, cv.THRESH_BINARY_INV)
    return thresholded

def align(image, template, crop=True):
    """
    If the template is larger than the cropped and aligned area, 
        may need to swap the images in the homography align step
    """
    MIN_MATCH_COUNT = 10
    FLANN_INDEX_KDTREE = 1

    image_height, image_width = image.shape[:2]

    # Create an instance of the SIFT aligner
    sift = cv.SIFT_create()
    
    # Compute keypoints for template
    template_keypoints, des1 = sift.detectAndCompute(template, None) 
    image_keypoints, des2 = sift.detectAndCompute(image,None) 

    # Find matches between images based on keypoints and descriptors
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,des2,k=2)
    
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)    

    # print('Number of good matches: {}'.format(len(good)))

    # Do we have enough good points? If so, proceeed, otherwise return 0
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([ template_keypoints[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ image_keypoints[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()
        template_h, template_w = template.shape
        pts = np.float32([ 
            [0,0],
            [0,template_h-1],
            [template_w-1,template_h-1],
            [template_w-1,0] 
        ]).reshape(-1,1,2)
        dst = cv.perspectiveTransform(pts,M)
        #imgCompare = cv.polylines(image,[np.int32(dst)],True,255,3, cv.LINE_AA)
    else:
        print("ERROR: Not enough matches found: {} / {}".format(len(good), MIN_MATCH_COUNT) )
        matchesMask = None
        return 
    
    # For viewing 
    # Extract points defining boundary rectangle around the device in the raw image
    rect = cv.minAreaRect(dst)
    bounding_points = cv.boxPoints(rect)
    bounding_points = np.intp(bounding_points)
    
    # Warp the template image to the found device size and location
    transformed_image = cv.warpPerspective(template, M, (image_width, image_height)) 
    # transformed_image = cv.warpPerspective(image, M, (template_w, template_h))

    if crop:
        [x,y,w,h] = cv.boundingRect(bounding_points)
        return transformed_image[y:y+h, x:x+w], bounding_points
    
    return transformed_image, bounding_points     

def image_diff_positive(image, template):
    """
    Show areas where printed area expands beyond the template 

    Shape of both should be 2D numpy arrays, not 3D
    Traces are represented as black pixels, on a white background 
    """
    # Use the template as a mask? 
    # return cv.bitwise_and(image, template, mask=cv.bitwise_not(template)) 
    return cv.bitwise_xor(image, template)

def image_diff_negative(image, template):
    """
    Incomplete 
    Show area where the printed area is smaller than the template

    Shape of both should be 2D numpy arrays, not 3D
    Traces are represented as black pixels, on a white background 
    """
    # Use the template as a mask? 
    # return cv.bitwise_and(cv.bitwise_not(image), cv.bitwise_not(template), mask=template) 
    return cv.bitwise_xor(image, template)

def filter(image, size=3):
    kernel_square = np.full((size,size), 1)
    # kernel_cross = np.array([
    #     [0,  1,  0],
    #     [1,  1,  1],
    #     [0,  1,  0],
    # ])
    img = cv.erode(image, kernel_square)
    img = cv.dilate(img, kernel_square)
    return img

def get_opens_and_shorts(positive_diff, negative_diff, min_area=10):
    """
    Requires shapes to be white on black
    1. Get blobs, filter by size 
    2. Get contours of blobs
    """
    params = cv.SimpleBlobDetector_Params()
    # Change thresholds
    # params.minThreshold = 128;
    # params.maxThreshold = 255;
    
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 100
    
    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.1
    
    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0.87
    
    # Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = 0.01

    detector = cv.SimpleBlobDetector_create(params)

    # positive_diff = cv.bitwise_not(positive_diff)

    # Find contours 
    keypoints1 = detector.detect(positive_diff)
    contours1, hierarchy1 = cv.findContours(positive_diff, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) 
    im1_with_keypoints = cv.drawKeypoints(positive_diff, keypoints1, np.array([]), (255,0,0), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # keypoints2 = detector.detect(negative_diff)
    # contours2, hierarchy2 = cv.findContours(negative_diff, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) 
    # im2_with_keypoints = cv.drawKeypoints(negative_diff, keypoints2, np.array([]), (0,0,255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


    # contours = {
    #     "positive": contours1,
    #     "negative": contours2
    #     }
    
 
    # Show keypoints
    return im1_with_keypoints

    # return contours

def contiguous(positive_diff, show_largest_n=5):
    output = cv.connectedComponentsWithStats(positive_diff)
    (numLabels, labels, stats, centroids) = output 
    # Get non-background, 
    # stats = stats[1:20] 
    # centroids = centroids[1:20] 
    color_diff = cv.cvtColor(positive_diff, cv.COLOR_GRAY2RGB)
    
    # Filter by top 10. Index 0 is the background so skip 
    stats_and_centroids = [item for item in zip(stats[1:], centroids[1:])] 
    sorted_stats = sorted(stats_and_centroids, key=lambda a: a[0][-1], reverse=True)[:10]
    
    # Draw circles 
    radius = 50
    edge_width=2
    filter_area = 200

    # import ipdb; ipdb.set_trace()
    
    for n in range(1, len(sorted_stats)):         
        if sorted_stats[n][0][-1] >= filter_area:
            color_diff = cv.circle(
                color_diff, 
                (int(sorted_stats[n][1][0]), int(sorted_stats[n][1][1])), 
                radius , 
                (255, 255, 0), 
                edge_width
            )

    return color_diff


if __name__ == "__main__":
    template = open_template('../data/StitchDemo/artwork/L1.bmp') 
    img_path = glob.glob('../data/StitchDemo/WorkflowRun_1/1_stitched/*_2_dispense.jpg')[0] 
    print("opening",img_path) 
    image = open_image(img_path) 

    img_thresholded = threshold(image)

    # Align and crop 
    transformed_template, bbox = align(img_thresholded, template, crop=True) 
    [x,y,w,h] = cv.boundingRect(bbox) 
    img_cropped = img_thresholded[y:y+h, x:x+w] 

    # Run a positive and negative diff
    image_diff_pos = image_diff_positive(img_cropped, transformed_template) 
    # image_diff_neg = image_diff_negative(img_cropped, transformed_template) 

    # Filter 
    image_diff_pos = filter(image_diff_pos, size=2)

    # Get the largest blobs 
    color_diff = contiguous(image_diff_pos)

    # Display
    # plt.imshow(opencv2matplotlib(color_diff))
    plt.imshow(color_diff)
    plt.show() 
    