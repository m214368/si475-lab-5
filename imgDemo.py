import math, rospy
from turtleAPI import robot
import cv2
import numpy as np

# make the robot and lists for tracking error
r = robot()
error_list = []
pi = math.pi

# pid
def pid_speed(kp, ki, kd, error, old_error, error_list):

    # add the error to the integral portion
    if len(error_list) > 5:
        error_list.pop()
        error_list.append(error)

    # calculate sum
    error_sum = 0
    for i in error_list:
        error_sum += i

    # kp portion + ki portion
    to_return = (kp * error) + (ki * error_sum)
    to_return += kd * (error - old_error)

    return to_return

def hunt(color):
    speed_limit = 1 # speed limit
    turn_limit = .2 # turn speed limit
    colormap = {"blue":[220,240],"green":[130,160],"purple":[290,320],"red":[-10,10],"yellow":[50,70]}
    bot = np.array([colormap[color][0]/2, 20, 10])
    top = np.array([colormap[color][1]/2,255,235])

    rate = rospy.Rate(30)

    #size = spin(r,top,bot,turn_limit,rate)
    size = 6
    
    r.drive(angSpeed=0, linSpeed=0)
    print("done with spin")
    print("largest blob: ",size)

    # loop until at position
    old_error = 0

    while True:
        image = r.getImage()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mapimage = cv2.inRange(hsv, bot, top)
        augimage = image
        augimage[:, :, 1] = np.bitwise_or(image[:, :, 1], mapimage)
        cv2.imshow('augmented',augimage)
        cv2.waitKey(1)
        # current pos
        current_pos = r.getPositionTup()
        current_angle = current_pos[2]
        
        height, width = mapimage.shape[0:2]
        total = cv2.countNonZero(mapimage)
        width = width//2 # integer division
        halfLeft = mapimage[:,:width]
        left = cv2.countNonZero(halfLeft)
        halfRight = mapimage[:,width:]
        right = cv2.countNonZero(halfRight)
        print ("total: "+str(total)+" left: "+str(left)+" right: "+str(right))

        # calculate angle speed and lin speed drive
        lin_speed = speed_limit
        
        # if less than 1/3rd of the original blob size found keep turning left
        # but with 0 lin_speed
        last_seen = 1 # 1 for left, -1 for right
        if (total < size/3):
            error = 100 * last_seen
            lin_speed = 0
        else:
            error = (left - right)/total
            last_seen = np.sign(error)

        if (total > 30000):
            lin_speed = 0
            if (abs(error) < 10):
                r.drive(angSpeed=0, linSpeed=0)
                print("done")
                return

        # speed
        ang_speed = pid_speed(.2, .01, .001, error, old_error, error_list)


        if (ang_speed > turn_limit):
            ang_speed = turn_limit

        ang_speed = ang_speed + (lin_speed/speed_limit)*np.sign(ang_speed)

        r.drive(angSpeed=ang_speed, linSpeed=lin_speed)
        print('speed: ' + str(ang_speed) + ' ' + str(lin_speed))

        # set old values
        old_error=error
        rate.sleep()
        print(' ')

def spin(r,top,bot,turn_limit,rate):
    # initial spin to find largest color blob
    cur_pos = r.getPositionTup()
    init_ang = cur_pos[2]
    
    size = 0
    
    stillSpin = True
    pastQuarter = False

    while stillSpin:
        cur_pos = r.getPositionTup()
        cur_ang = cur_pos[2]
        image = r.getImage()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mapimage = cv2.inRange(hsv, bot, top)
        augimage = image
        augimage[:, :, 1] = np.bitwise_or(image[:, :, 1], mapimage)
        cv2.imshow('augmented',augimage)
        cv2.waitKey(1)
        height, width = mapimage.shape[0:2]
        total = cv2.countNonZero(mapimage)
        if total > size:
            size = total
        width = width//2 # integer division
        halfLeft = mapimage[:,:width]
        left = cv2.countNonZero(halfLeft)
        halfRight = mapimage[:,width:]
        right = cv2.countNonZero(halfRight)
        r.drive(angSpeed=turn_limit, linSpeed=0)

        # For debugging:
        print ("total: "+str(total)+" left: "+str(left)+" right: "+str(right))
        #print("Angle Diff: " + str(abs(cur_ang-init_ang)))

        angleDiff = abs(cur_ang-init_ang)

        # the robot has spun a quarter turn
        if(angleDiff > pi/2):
            pastQuarter = True

        # when the robot has done a quarter turn and the
        # diff btwn original and current is close to 0, we are
        # done turning
        if(pastQuarter and angleDiff < 0.1):
            print("done turning")
            stillSpin = False

        rate.sleep()
        
    return size

def Blob(): 
    # https://learnopencv.com/blob-detection-using-opencv-python-c/
    # https://www.geeksforgeeks.org/find-circles-and-ellipses-in-an-image-using-opencv-python/
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()
    
    # Change thresholds
    params.minThreshold = 10;
    params.maxThreshold = 200;

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 1500

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.87

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.01

    # Create a detector with the parameters
    ver = (cv2.__version__).split('.')
    if int(ver[0]) < 3 :
        detector = cv2.SimpleBlobDetector(params)
    else :
        detector = cv2.SimpleBlobDetector_create(params)

color = raw_input("What color to hunt:")
hunt(color)
