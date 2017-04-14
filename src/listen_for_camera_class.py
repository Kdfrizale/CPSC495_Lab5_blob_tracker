#!/usr/bin/env python
import roslib
from cv_bridge import CvBridge, CvBridgeError
import rospy
from std_msgs.msg import Float32
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

hh='Hue High'
hl='Hue Low'
sh='Saturation High'
sl='Saturation Low'
vh='Value High'
vl='Value Low'

cv2.namedWindow('image')

class Camera_Listener:
    def __init__(self):
        self.pubvel = rospy.Publisher('makethisupvel', Float32, queue_size=10)
        self.pubang = rospy.Publisher('makethisupang', Float32, queue_size=10)

        self.myBridge = CvBridge()


        cv2.createTrackbar(hl, 'image',0,179,nothing)
        cv2.createTrackbar(hh, 'image',0,179,nothing)
        cv2.createTrackbar(sl, 'image',0,255,nothing)
        cv2.createTrackbar(sh, 'image',0,255,nothing)
        cv2.createTrackbar(vl, 'image',0,255,nothing)
        cv2.createTrackbar(vh, 'image',0,255,nothing)
        cv2.waitKey(0)

    def findBlob(self,imageReceived):
        ##Convert ROS NODE PICTURE TO CV2 FORMAT
        cv_image = self.myBridge.imgmsg_to_cv2(imageReceived,"bgr8")
        frame = cv_image
        Gaussianframe=cv2.GaussianBlur(frame,(5,5),0)
        #convert to HSV from BGR

        hsv=cv2.cvtColor(Gaussianframe, cv2.COLOR_BGR2HSV)

        cv2.imshow("raw hsv",hsv)


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
        cv2.imshow("inRange mask",mask)
        cv2.waitKey(0)
        res = cv2.bitwise_and(Gaussianframe,Gaussianframe, mask =mask)
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            #print(M["m00"])
            if not(M["m00"] == 0):
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                ball_x =int(M["m10"] / M["m00"])
                ball_y =int(M["m01"] / M["m00"])
                ###Calculate how to move the robot to aling ball in image
                Ydesired = 240 ###Half of the height of the image
                Xdesired = 320 ###Half of the width of the image
                Kpv = -1
                Kpw = 1
                ###Publish command
                velocityData = Float32()
                angularData = Float32()
                velocityData.data = float(Kpv*(Ydesired - ball_y))
                angularData.data = float(Kpw*(Xdesired - ball_x))
                self.pubang.publish(angularData)
                self.pubvel.publish(velocityData)


            if radius > 10:
                cv2.circle(Gaussianframe, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(Gaussianframe, center, 1, (0, 0, 255), -1)

        cv2.imshow('image', res)
        #cv2.imshow('Gaussianframe', Gaussianframe)
        k = cv2.waitKey(5) & 0xFF



def listener_for_camera():
    rospy.init_node('listener_for_camera', anonymous=True)
    myCameraListener = Camera_Listener()

    rospy.Subscriber("/turtlebot/camera/rgb/image_raw", Image, myCameraListener.findBlob)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener_for_camera()









#cv2.destroyAllWindows()
