import numpy as np
import cv2

img = cv2.imread('trash.jpg')
cv2.imshow('image',img)

Gaussianframe=cv2.GaussianBlur(img,(5,5),0)


hsv=cv2.cvtColor(Gaussianframe, cv2.COLOR_BGR2HSV)
cv2.imshow('blur1', Gaussianframe)

hul=0
huh=255
sal=0
sah=255
val=0
vah=255
#make array for final values
HSVLOW=np.array([hul,sal,val])
HSVHIGH=np.array([huh,sah,vah])
#apply the range on a mask
mask = cv2.inRange(hsv,HSVLOW, HSVHIGH)
	
cnts = cv2.findContours(Gaussianframe, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
center = None
cv2.imshow('blur2', Gaussianframe)


if len(cnts) > 0:
    c = max(cnts, key=cv2.contourArea)
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    #print(M["m00"])
    if not(M["m00"] == 0):
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        print center
    if radius > 10:
        cv2.imshow('blur3', Gaussianframe) 
        cv2.circle(Gaussianframe, (int(x), int(y)), int(radius),
            (0, 255, 255), 2)
        cv2.circle(Gaussianframe, center, 1, (0, 0, 255), -1)
        cv2.imshow('blur4', Gaussianframe)    





cv2.imshow('blur', Gaussianframe)



k = cv2.waitKey(0) & 0xFF
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()

