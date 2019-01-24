import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow('image')

cv2.createTrackbar('DownH1','image', 0, 255, nothing)
cv2.createTrackbar('UpH1','image', 5, 255, nothing)

cv2.createTrackbar('DownS','image', 0, 255, nothing)
cv2.createTrackbar('UpS','image', 255, 255, nothing)

cv2.createTrackbar('DownV','image', 0, 255, nothing)
cv2.createTrackbar('UpV','image', 255, 255, nothing)

#cv2.createTrackbar('DownH2','image', 175, 255, nothing)
#cv2.createTrackbar('UpH2','image', 255, 255, nothing)

cv2.createTrackbar('Сore1','image', 3, 255, nothing)
cv2.createTrackbar('Core2','image', 3, 255, nothing)
while(1):



    DownH1 = cv2.getTrackbarPos('DownH1','image')
    UpH1 = cv2.getTrackbarPos('UpH1','image')

    DownS = cv2.getTrackbarPos('DownS','image')
    UpS = cv2.getTrackbarPos('UpS','image')

    DownV = cv2.getTrackbarPos('DownV','image')
    UpV = cv2.getTrackbarPos('UpV','image')
    
    #DownH2 = cv2.getTrackbarPos('DownH2','image')
    #UpH2 = cv2.getTrackbarPos('UpH2','image')

    Core1 = cv2.getTrackbarPos('Сore1','image')
    Core2 = cv2.getTrackbarPos('Core2','image')

    # Take each frame
    _, frame = cap.read()

    
    # Convert BGR to HSV
    #
   # blur = cv2.GaussianBlur(frame,(5,5),0)
   # median = cv2.medianBlur(blur,5)
    median = cv2.medianBlur(frame,3)
   # blur = cv2.GaussianBlur(median,(9,9),0)

    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)

    equ = cv2.equalizeHist(hsv)
    # define range of blue color in HSV
    #lower_green = np.array([113,0,0])
    #upper_green = np.array([131,255,255])

    lower_value = np.array([DownH1,DownS,DownV])
    upper_value = np.array([UpH1,UpS,UpV])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(equ, lower_value, upper_value)
    #
    kernel = np.ones((Core1,Core2), np.uint8)
    erosion = cv2.erode(mask, kernel, iterations = 1)    
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    



    #mask = cv2.medianBlur(mask,21)
    # __mask = cv2.threshold(mask,200,255,0)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= opening)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('image',res)
    cv2.imshow('erosion', erosion)
    cv2.imshow('opening', opening)
    #cv2.imshow('Gauss', blur)
    cv2.imshow('median', median)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()