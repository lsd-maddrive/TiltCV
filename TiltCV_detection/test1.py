import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow('image')

cv2.createTrackbar('unknow1','image',  30, 190, nothing)
cv2.createTrackbar('unknow2','image', 700, 1000, nothing)

cv2.createTrackbar('param1','image', 1, 1000, nothing)
cv2.createTrackbar('param2','image', 1, 1000, nothing)

cv2.createTrackbar('minRadius','image', 1, 1000, nothing)
cv2.createTrackbar('maxRadius','image', 1, 1000, nothing)

#cv2.createTrackbar('DownH2','image', 175, 255, nothing)
#cv2.createTrackbar('UpH2','image', 255, 255, nothing)



while(1):



    unknow1 = cv2.getTrackbarPos('unknow1','image')
    unknow2 = cv2.getTrackbarPos('unknow2','image')

    param1 = cv2.getTrackbarPos('param1','image')
    param2 = cv2.getTrackbarPos('param2','image')

    minRadius = cv2.getTrackbarPos('minRadius','image')
    maxRadius = cv2.getTrackbarPos('maxRadius','image')

    _, frame = cap.read()

    #median = cv2.medianBlur(frame,5)

    blur = cv2.GaussianBlur(frame,(3,3),0)

    blur = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, unknow1, unknow2, param1, param2, minRadius, maxRadius)
   
    #hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
            
            circles = np.round(circles[0, :]).astype("int")
     
        # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                

                # cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                # cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

                cv2.circle(blur, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(blur, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        



    #cv2.imshow('hsv', hsv)
    cv2.imshow('image',blur)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()