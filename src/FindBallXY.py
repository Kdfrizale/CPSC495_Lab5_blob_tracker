#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from collections import deque
import cv2
import numpy as np
import argparse
#np.set_printoptions(threshold='nan')
#optional argument
def nothing(x):
    pass

cv2.namedWindow('image')

def draw_flow(img, flow, step=16): #step = 16, named parameter
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int) #Creating the grid of flow points (40, 30) i.e. 1200 points
    #print y
    #print x
    fx, fy = flow[y,x].T #flow value for each point 
    #print flow[y,x].shape
    #print(flow[[10,1,2],[10]])
    #print fx.shape
   
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    #print(vis)
    cv2.polylines(vis, lines, 0, (0, 255, 0)) #draws vector lines based on the points (x1, y1), (x2, y2)

    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis



def findBlob(imageReceived):
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
         help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
         help="max buffer size")
    args = vars(ap.parse_args())

    pts = deque(maxlen=args["buffer"])

    #easy assigments
    hh='Hue High'
    hl='Hue Low'
    sh='Saturation High'
    sl='Saturation Low'
    vh='Value High'
    vl='Value Low'

    cv2.createTrackbar(hl, 'image',0,179,nothing)
    cv2.createTrackbar(hh, 'image',0,179,nothing)
    cv2.createTrackbar(sl, 'image',0,255,nothing)
    cv2.createTrackbar(sh, 'image',0,255,nothing)
    cv2.createTrackbar(vl, 'image',0,255,nothing)
    cv2.createTrackbar(vh, 'image',0,255,nothing)

    #cap = cv2.VideoCapture(0)
    #ret, prev = cap.read()
    prev = cv2.imread("trash.jpg")
    prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    show_hsv = False
    show_glitch = False
    cur_glitch = prev.copy()

    while(1):
        #ret, frame = cap.read()
        frame = cv2.imread("trash.jpg")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        #print(len(flow[1][0]))
        prevgray = gray


        Gaussianframe=cv2.GaussianBlur(frame,(5,5),0)
        #convert to HSV from BGR
        hsv=cv2.cvtColor(Gaussianframe, cv2.COLOR_BGR2HSV)

        #cv2.imshow('flow_mask', draw_flow(mask, flow))
        #read trackbar positions for all
        hul=cv2.getTrackbarPos(hl, 'image')
        huh=cv2.getTrackbarPos(hh, 'image')
        sal=cv2.getTrackbarPos(sl, 'image')
        sah=cv2.getTrackbarPos(sh, 'image')
        val=cv2.getTrackbarPos(vl, 'image')
        vah=cv2.getTrackbarPos(vh, 'image')
        #make array for final values
        HSVLOW=np.array([hul,sal,val])
        HSVHIGH=np.array([huh,sah,vah])

        #apply the range on a mask
        mask = cv2.inRange(hsv,HSVLOW, HSVHIGH)
        res = cv2.bitwise_and(Gaussianframe,Gaussianframe, mask =mask)
        cv2.imshow('flow_mask', draw_flow(mask, flow))
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        #For finding contours and drawing circle around focal point
        if len(cnts) > 0:
         c = max(cnts, key=cv2.contourArea)
         ((x, y), radius) = cv2.minEnclosingCircle(c)
         M = cv2.moments(c)
         #print(M["m00"])
         if not(M["m00"] == 0):
             center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
         if radius > 10:
             cv2.circle(Gaussianframe, (int(x), int(y)), int(radius),
                  (0, 255, 255), 2)
             cv2.circle(Gaussianframe, center, 1, (0, 0, 255), -1)


        pts.appendleft(center)

        cv2.imshow('image', res)
        cv2.imshow('yay', Gaussianframe)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
             break








def FindBallXY():
    rospy.init_node('FindBallXY, anonymous=True)

    rospy.Subscriber("/turtlebot/camera/rgb/image_raw", Image, findBlob)

    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()

















cv2.destroyAllWindows()