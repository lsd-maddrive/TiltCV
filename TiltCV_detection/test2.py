import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow('image')

cv2.createTrackbar('dp','image', 30, 190, nothing)
cv2.createTrackbar('minDist','image', 700, 1000, nothing)

cv2.createTrackbar('param1','image', 1, 1000, nothing)
cv2.createTrackbar('param2','image', 1, 1000, nothing)

cv2.createTrackbar('minRadius','image', 1, 1000, nothing)
cv2.createTrackbar('maxRadius','image', 1, 1000, nothing)

#cv2.createTrackbar('DownH2','image', 175, 255, nothing)
#cv2.createTrackbar('UpH2','image', 255, 255, nothing)



while(1):



    dp = cv2.getTrackbarPos('dp','image')
    minDist = cv2.getTrackbarPos('minDist','image')

    param1 = cv2.getTrackbarPos('param1','image')
    param2 = cv2.getTrackbarPos('param2','image')

    minRadius = cv2.getTrackbarPos('minRadius','image')
    maxRadius = cv2.getTrackbarPos('maxRadius','image')

    _, frame = cap.read()

    #median = cv2.medianBlur(frame,5)

    blur = cv2.GaussianBlur(frame,(3,3),0)

    blur = cv2.cvtColor(blur, cv2.COLOR_RGB2GRAY)

    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp, minDist, param1, param2, minRadius, maxRadius)
   
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
    # draw the outer circle
     cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
     cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
        



    #cv2.imshow('hsv', hsv)
    cv2.imshow('image',frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()