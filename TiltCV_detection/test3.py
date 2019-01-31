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


    circles = cv2.HoughCircles(edges1, cv2.HOUGH_GRADIENT, minrad, maxrad)
    
    if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
        
        circles = np.round(circles[0, :]).astype("int")
 
    # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            

            # cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            # cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            cv2.circle(edges1, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(edges2, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    cv2.imshow('Canny_frame', edges2)
    cv2.imshow('Canny_Equ', edges1)
    cv2.imshow('Equ', equ)
    cv2.imshow('Frame', new_frame)
    # cv2.imshow('image', res2)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()