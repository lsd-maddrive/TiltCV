import cv2
import numpy as np
from matplotlib import pyplot as plt

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow('image')

# cv2.createTrackbar('clipLimit', 'image',20,1000, nothing)
# cv2.createTrackbar('tileGridSize', 'image',8,100, nothing)
while (1):

    # cliptlimit = cv2.getTrackbarPos('clipLimit', 'image')

    # tiltegridsize = cv2.getTrackbarPos('tileGridSize', 'image')
    
    # cliptlimit = cliptlimit / 10

    _, frame = cap.read()

    new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(new_frame,100,200)

    cv2.imshow('new_frame',new_frame)

    cv2.imshow('edges',edges)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()