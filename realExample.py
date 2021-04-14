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
