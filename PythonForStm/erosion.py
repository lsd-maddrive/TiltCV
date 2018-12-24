import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    #lower_green = np.array([113,0,0])
    #upper_green = np.array([131,255,255])

    lower_green = np.array([161&0,0,0])
    upper_green = np.array([189&10,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_green, upper_green)
    #
    kernel = np.ones((5,5), np.uint8)
    erosion = cv2.erode(mask, kernel, iterations = 1)    
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    #mask = cv2.medianBlur(mask,21)
    # __mask = cv2.threshold(mask,200,255,0)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= opening)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('erosion', erosion)
    cv2.imshow('opening', opening)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()