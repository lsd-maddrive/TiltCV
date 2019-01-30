import cv2
import numpy as np
import argparse
import serial


def nothing(x):
    pass

cap = cv2.VideoCapture(0)

ser = serial.Serial('/dev/ttyUSB0',115200,timeout=1)

first_serv = 1
second_serv = 2

value_PWM_first_serv = 500
value_PWM_second_serv = 500

send_pkg = bytes([ord('#'), first_serv]) + value_PWM_first_serv.to_bytes(2, byteorder='big')
ser.write(send_pkg)

send_pkg = bytes([ord('#'), second_serv]) + value_PWM_second_serv.to_bytes(2, byteorder='big')
ser.write(send_pkg)

x_center = 320
y_center = 240

center_deviation = 5

alpha = 0.4
beta = 1 - alpha





cv2.namedWindow('image')

cv2.createTrackbar('DownH1','image', 65, 255, nothing)
cv2.createTrackbar('UpH1','image', 92, 255, nothing)

cv2.createTrackbar('DownS','image', 55, 255, nothing)
cv2.createTrackbar('UpS','image', 255, 255, nothing)

cv2.createTrackbar('DownV','image', 8, 255, nothing)
cv2.createTrackbar('UpV','image', 255, 255, nothing)

cv2.createTrackbar('erosion','image', 4, 20, nothing)
cv2.createTrackbar('dilation','image', 4, 20, nothing)

cv2.createTrackbar('minrad','image', 3, 255, nothing)
cv2.createTrackbar('maxrad','image', 700, 1000, nothing)

cv2.createTrackbar('deviation','image', 180, 240, nothing)

x = None
y = None

while(1):



    DownH1 = cv2.getTrackbarPos('DownH1','image')
    UpH1 = cv2.getTrackbarPos('UpH1','image')

    DownS = cv2.getTrackbarPos('DownS','image')
    UpS = cv2.getTrackbarPos('UpS','image')

    DownV = cv2.getTrackbarPos('DownV','image')
    UpV = cv2.getTrackbarPos('UpV','image')

    erosion_iter = cv2.getTrackbarPos('erosion','image')
    dilation_iter = cv2.getTrackbarPos('dilation','image')

    minrad = cv2.getTrackbarPos('minrad','image')
    maxrad = cv2.getTrackbarPos('maxrad','image')

    center_deviation = cv2.getTrackbarPos('deviation','image')

    x_right_deviation = x_center + center_deviation
    x_left_deviation = x_center - center_deviation
    y_up_deviation = y_center - center_deviation
    y_down_deviation = y_center + center_deviation

    _, frame = cap.read()
    output = frame.copy()

    newhogh = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) ####

    blur = cv2.GaussianBlur(frame,(3,3),0)
   
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower_value = np.array([DownH1,DownS,DownV])
    upper_value = np.array([UpH1,UpS,UpV])
    res = cv2.inRange(hsv, lower_value, upper_value)

    newres = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)

    kernel = np.ones((3,3), np.uint8)

    erosion = cv2.erode(res, kernel, iterations = erosion_iter)

    opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)

    dilation = cv2.dilate(erosion, kernel, iterations = dilation_iter)

    newdilation = cv2.cvtColor(dilation, cv2.COLOR_GRAY2BGR)

    processed = cv2.bitwise_and(frame,frame, mask = dilation)


    x = None
    y = None



    #create circle
    gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, minrad, maxrad)
    
    (x,y),radius = cv2.minEnclosingCircle(gray)

    center = (int(x),int(y))
    radius = int(radius)
    cv2.Circle(frame,center,radius,(0,255,0),2)

    cv2.imshow('image',output )
    cv2.imshow('frame', dilation)
    cv2.imshow('original', frame)
    cv2.imshow('circle', processed)
    cv2.imshow('erosion',erosion )
    cv2.imshow('dilation',dilation )
    cv2.imshow('hsv', hsv )
    cv2.imshow('res', res )
    tst = np.hstack((erosion, dilation))
    tst1 = np.hstack((processed, frame))
    cv2.imshow('tst', tst)
    cv2.imshow('tst1', tst1)



    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()