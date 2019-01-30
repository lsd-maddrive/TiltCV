import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)


while (1):

    


    _, frame = cap.read()

    new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    #adapt equalize
    clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8,8)) 
    cl1 = clahe.apply(new_frame)

    # sample equalize
    equ = cv2.equalizeHist(new_frame)

    edges1 = cv2.Canny(equ,100,200)

    edges2 = cv2.Canny(new_frame,100,200)

    cv2.imshow('Canny_frame', edges2)
    cv2.imshow('Canny_Equ', edges1)
    cv2.imshow('Equ', equ)
    cv2.imshow('Frame', new_frame)
    # cv2.imshow('image', res2)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()