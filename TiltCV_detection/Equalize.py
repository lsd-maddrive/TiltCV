import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow('image')

cv2.createTrackbar('clipLimit', 'image',20,1000, nothing)
cv2.createTrackbar('tileGridSize', 'image',8,100, nothing)
while (1):

    cliptlimit = cv2.getTrackbarPos('clipLimit', 'image')

    tiltegridsize = cv2.getTrackbarPos('tileGridSize', 'image')
    
    cliptlimit = cliptlimit / 10

    _, frame = cap.read()

    new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    #adapt equalize
    clahe = cv2.createCLAHE(clipLimit=cliptlimit, tileGridSize=(tiltegridsize,tiltegridsize)) 
    cl1 = clahe.apply(new_frame)

    # sample equalize
    equ = cv2.equalizeHist(new_frame)

    res1 = np.hstack((new_frame,equ))
    res2 = np.hstack((new_frame, cl1))
    cv2.imshow('res1', res1)
    cv2.imshow('image', res2)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()