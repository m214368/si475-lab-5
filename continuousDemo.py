#continuously drive until you get hit and then turn and continue

import rospy
from turtleAPI import robot
from time import sleep


gas=.25
wheel=.75
back=3
forward=2


#try:
if True:
  #print("creating robot")
  r= robot()
  rate = rospy.Rate(10)

  #drive forward
  r.drive(angSpeed=0,linSpeed=gas)

  newBump = True
  while not rospy.is_shutdown():
    #check if bump has been detected
    s = r.getBumpStatus()
    print(s)
    #print(s[list(s.keys)[0]])
    if (s["state"] == 1 and newBump): #bump detected
      newBump = False
      r.drive(angSpeed=0,linSpeed=-gas)
      sleep(back)
      if (s["bumper"] == 2): #right side bumper
        r.drive(angSpeed=wheel,linSpeed=gas)
      elif (s["bumper"] == 0): #left side bumper
        r.drive(angSpeed=-wheel,linSpeed=gas)
      else: #middle bumper
        r.drive(angSpeed=wheel,linSpeed=0) #positive is left
        
      sleep(forward)
      r.drive(angSpeed=0,linSpeed=gas)
      
    rate.sleep()      
    if s["state"] == 0:
      newBump = True
      
#except Exception as e:
#  print(e)
#  rospy.loginto("node now terminated")
