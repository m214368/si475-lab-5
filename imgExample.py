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
    dpth=r.getDepth()
    img=r.getImage()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #outhsv = cv2.inRange(hsv, np.array([210/2, 15, 20]), np.array([240/2,255,255]))
    #img[:, :, 1] = np.bitwise_or(img[:, :, 1], outhsv)
    print(type(dpth))
    cv2.imshow("Image",dpth)
    print(dpth)
    cv2.waitKey(1)
    rate.sleep()
except Exception as e:
  print(e)
  rospy.loginto("node now terminated")
