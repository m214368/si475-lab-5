#continuously drive until you get too close and then turn and continue

import rospy
from turtleAPI import robot
from time import sleep
import numpy as np


gas=.25
wheel=.75


#try:
if True:

  #print("creating robot")
  r= robot()
  rate = rospy.Rate(10)

  image = r.getImage()
  height, width = image.shape[0:2]


  #drive forward
  r.drive(angSpeed=0,linSpeed=gas)

  while not rospy.is_shutdown():
    #check min distance to walls

    dpth=r.getDepth()
    middle_row = dpth[height/2,:]
    print(middle_row)
    if len(middle_row[np.nonzero(middle_row)]) > 0:
      min = np.nanmin(middle_row[np.nonzero(middle_row)])
    else:
      min = 1200
    if ( min < 1000 ):
       r.drive(angSpeed=wheel,linSpeed=0)
    else:
       r.drive(angSpeed=0,linSpeed=gas)
    rate.sleep()      
      
#except Exception as e:
#  print(e)
#  rospy.loginto("node now terminated")
