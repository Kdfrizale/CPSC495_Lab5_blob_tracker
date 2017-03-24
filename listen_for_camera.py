#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from collections import deque
import cv2
import numpy as np
import argparse
#np.set_printoptions(threshold='nan')
#optional argument
def nothing(x):
    pass

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def findBlob(imageReceived):
    ##ROS SETUP FOR PUBLISHER
    pub = rospy.Publisher('chatter', String, queue_size=10)###CHANGE TO CORRECT TOPIC TO PUBLISH TO
    

    ##CODE TO GET CENTER OF BLOB
    ret, frame = imageReceived
	Gaussianframe=cv2.GaussianBlur(frame,(5,5),0)
    #convert to HSV from BGR
	hsv=cv2.cvtColor(Gaussianframe, cv2.COLOR_BGR2HSV)

	#cv2.imshow('flow_mask', draw_flow(mask, flow))
	#read trackbar positions for all
	hul=cv2.getTrackbarPos(hl, 'image')#####Change these to these values to those of the ball being found
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


	###Publish center
	pub.publish(center) ###############################May need to format center first

##	k = cv2.waitKey(5) & 0xFF
##        if k == 27:
##            break
    

def listener_for_camera():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener_for_camera', anonymous=True)

    rospy.Subscriber("chatter", String, findBlob)######################CHange this to get camera INFO for turtlebot

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener_for_camera()
