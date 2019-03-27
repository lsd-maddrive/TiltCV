import cv2
import numpy as np
import argparse
import time

 
import track_bar as tb
import find_object as fo
import control_system as cs
import serial_connection as sc
import image_processing as ip
import matplotlib.pyplot as plt



cap = cv2.VideoCapture(0)
tb.createTrackbar()

value_PWM_first_serv = 500
value_PWM_second_serv = 500

ser = sc.InitSerial(value_PWM_first_serv,value_PWM_second_serv)

file = open('valuet_error.txt', 'w')
flag_start_system_control = 0
x_control_syst = []
y_control_syst = []
time_control_syst = []
while(1):

    _, frame = cap.read()
    output = frame.copy()

    output,x_real,y_real = fo.finding_a_circle_around_the_contour(frame)

    dilation = ip.processing_morphological_operators(frame)
    
    if flag_start_system_control == 1:
    	
        value_PWM_first_serv, value_PWM_second_serv = cs.check_deviation(x_real,y_real,value_PWM_first_serv,value_PWM_second_serv,ser)
        x_control_syst, y_control_syst,time_control_syst = cs.write_value_error(x_real,y_real,x_control_syst, y_control_syst, start_time,time_control_syst, file)
    
    cv2.imshow('image',output)

    cv2.imshow('dilation', dilation)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        file.close()
        break

    if k == 13:
        start_time = time.time()
        flag_start_system_control = 1

   
    if k == 32:

        flag_start_system_control = 0
        print(type(x_control_syst))
        print()
        print(type(len(x_control_syst)))
        
        plt.plot(time_control_syst,x_control_syst)
        plt.plot(time_control_syst,y_control_syst)
        plt.show()

        x_control_syst = []
        y_control_syst = []
        time_control_syst = []
        

cv2.destroyAllWindows()