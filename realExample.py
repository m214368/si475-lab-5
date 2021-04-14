import rospy
from turtleAPI import robot
import cv2
import numpy as np
np.set_printoptions(threshold=np.inf)



try:
  print("creating robot")
  r= robot()
  rate = rospy.Rate(1)
  while not rospy.is_shutdown():
    #dpth=r.getDepth()
    img=r.getImage()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mapimg = cv2.inRange(hsv, np.array([250/2, 20, 70]), np.array([305/2,255,255]))
    img[:, :, 1] = np.bitwise_or(img[:, :, 1], mapimg)
    
    #start blob detection
    params = cv2.SimpleBlobDetector_Params()
    
    # Change thresholds
    params.minThreshold = 10;
    params.maxThreshold = 200;
    
    # Filter by Area.
    params.filterByArea = False
    params.minArea = 300
    
    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.01
    
    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.01
    
    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.01
    
    # Create a detector with the parameters
    ver = (cv2.__version__).split('.')
    if int(ver[0]) < 3 :
        detector = cv2.SimpleBlobDetector(params)
    else :
        detector = cv2.SimpleBlobDetector_create(params)
        
    keypoints = detector.detect(mapimg)
    blank = np.zeros((1, 1)) 
    blobs = cv2.drawKeypoints(img, keypoints, blank, (0, 0, 255),
                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    number_of_blobs = len(keypoints)
    text = "Number of Circular Blobs: " + str(len(keypoints))
    cv2.putText(blobs, text, (20, 550),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)
    
    # Show blobs
    cv2.imshow("Filtering Circular Blobs Only", blobs)
    #print(type(dpth))
    #cv2.imshow("Image",dpth)
    #print(dpth)
    cv2.waitKey(1)
    rate.sleep()
except Exception as e:
  print(e)
  rospy.loginto("node now terminated")

import cv2
import numpy as np

img = cv2.imread('rbv2g.jpg',0)
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,10,
                            param1=50,param2=12,minRadius=0,maxRadius=20)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()

im = cv2.imread('extract_blue.jpg')
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im_gauss = cv2.GaussianBlur(imgray, (5, 5), 0)
ret, thresh = cv2.threshold(im_gauss, 127, 255, 0)
# get contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contours_area = []
# calculate area and filter into new array
for con in contours:
    area = cv2.contourArea(con)
    if 1000 < area < 10000:
        contours_area.append(con)
        
contours_cirles = []

# check if contour is of circular shape
for con in contours_area:
    perimeter = cv2.arcLength(con, True)
    area = cv2.contourArea(con)
    if perimeter == 0:
        break
    circularity = 4*math.pi*(area/(perimeter*perimeter))
    print circularity
    if 0.7 < circularity < 1.2:
        contours_cirles.append(con)