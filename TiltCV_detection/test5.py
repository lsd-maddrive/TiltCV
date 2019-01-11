import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow('image')

cv2.createTrackbar('DownH1','image', 106, 255, nothing)
cv2.createTrackbar('UpH1','image', 149, 255, nothing)

cv2.createTrackbar('DownS','image', 0, 255, nothing)
cv2.createTrackbar('UpS','image', 255, 255, nothing)

cv2.createTrackbar('DownV','image', 0, 255, nothing)
cv2.createTrackbar('UpV','image', 255, 255, nothing)

#cv2.createTrackbar('DownH2','image', 175, 255, nothing)
#cv2.createTrackbar('UpH2','image', 255, 255, nothing)

cv2.createTrackbar('erosion','image', 1, 20, nothing)
cv2.createTrackbar('dilation','image', 1, 20, nothing)
while(1):



    DownH1 = cv2.getTrackbarPos('DownH1','image')
    UpH1 = cv2.getTrackbarPos('UpH1','image')

    DownS = cv2.getTrackbarPos('DownS','image')
    UpS = cv2.getTrackbarPos('UpS','image')

    DownV = cv2.getTrackbarPos('DownV','image')
    UpV = cv2.getTrackbarPos('UpV','image')

    erosion_iter = cv2.getTrackbarPos('erosion','image')
    dilation_iter = cv2.getTrackbarPos('dilation','image')

    _, frame = cap.read()

    #median = cv2.medianBlur(frame,5)

    #blur = cv2.GaussianBlur(frame,(5,5),0)
    #hsv = cv2.cvtColor(blur, cv2.COLOR_RGB2HSV)
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    lower_value = np.array([DownH1,DownS,DownV])
    upper_value = np.array([UpH1,UpS,UpV])

    res = cv2.inRange(hsv, lower_value, upper_value)

    kernel = np.ones((5,5), np.uint8)

    erosion = cv2.erode(res, kernel, iterations = erosion_iter)


    opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)

    dilation = cv2.dilate(erosion, kernel, iterations = dilation_iter)

    processed = cv2.bitwise_and(frame,frame, mask = dilation)



    cv2.imshow('hsv', hsv)
    cv2.imshow('res', res)
    cv2.imshow('image',processed)
    cv2.imshow('frame', dilation)
    cv2.imshow('original', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()