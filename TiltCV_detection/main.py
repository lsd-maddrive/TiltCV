import cv2
import numpy as np
import argparse

 
import track_bar as tb
import find_object as fo
import control_system as cs
import serial_connection as sc



cap = cv2.VideoCapture(0)
tb.createTrackbar()

value_PWM_first_serv = 500
value_PWM_second_serv = 500

ser = sc.InitSerial(value_PWM_first_serv,value_PWM_second_serv)

while(1):

    _, frame = cap.read()
    output = frame.copy()

    output,x_real,y_real = fo.finding_a_circle_around_the_contour(frame)

    value_PWM_first_serv, value_PWM_second_serv = cs.check_deviation(x_real,y_real,value_PWM_first_serv,value_PWM_second_serv,ser)
    cv2.imshow('image',output)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()