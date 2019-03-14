import cv2
import numpy as np
import argparse

import track_bar as tb
import image_processing as ip
import find_object as fo



cap = cv2.VideoCapture(0)
tb.createTrackbar()


while(1):

    _, frame = cap.read()
    output = frame.copy()

    fo.finding_a_circle_around_the_contour(frame)

    cv2.imshow('image',output )
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()