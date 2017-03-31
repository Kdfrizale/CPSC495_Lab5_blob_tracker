#!/usr/bin/env python
from collections import deque
import cv2
import numpy as np
import argparse

#np.set_printoptions(threshold='nan')
#optional argument


def nothing(x):
    pass


while(1):
    frame = cv2.imread('trash.jpg')
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
                print center
            

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
