import cv2
import numpy as np
import argparse
import time
import json

import skfuzzy as fuzz
from skfuzzy import control as System_fuzzy

import track_bar as tb
import find_object as fo
import control_system as cs
import serial_connection as sc
import image_processing as ip
import matplotlib.pyplot as plt
import plot_graph as pg
import for_measurements as fm



        


    
cap = cv2.VideoCapture(0)
tb.createTrackbar()

start_time = 0 

value_PWM_first_serv = 500
value_PWM_second_serv = 500

ser = sc.InitSerial(value_PWM_first_serv,value_PWM_second_serv)


flag_start_system_control = 0

x_control_syst = []
y_control_syst = []
time_control_syst = []

x_control_syst_reserv = []
y_control_syst_reserv = []
time_control_syst_reserv = []

number_of_measurements = 0

x_center = 320
y_center = 240

flag_measur = 0
flag_syst_contr = 0

PWM_output_limit, PWM_MF_change_value_1, high_value_fuzzy, medium_value_fuzzy = tb.getFuzzy()

fuzzy_syst_for_y = cs.fuzzy_control_init_for_y(30, 20, 200, 150)
fuzzy_syst_for_x = cs.fuzzy_control_init_for_x(40, 20, 200, 150)

count = 0
time_control_system_measurements =0
time_system_control = 0
flag_new_measurements = 1

while(1):

    _, frame = cap.read()
    # output = frame.copy()

    frame,x_real,y_real = fo.finding_a_circle_around_the_contour(frame)
    if x_real and y_real is not None:
        x_error = x_center - x_real
        y_error = y_center - y_real
        
        if flag_syst_contr == 1:

            value_PWM_first_serv = cs.fuzzy_control_get_output_for_x(fuzzy_syst_for_x,x_error,value_PWM_first_serv,ser)
            value_PWM_second_serv = cs.fuzzy_control_get_output_for_y(fuzzy_syst_for_y,y_error,value_PWM_second_serv,ser)

    cv2.imshow('image',frame)

    k = cv2.waitKey(5) & 0xFF
    
    if k == 27:
        
        break

    if k == 13:

        flag_syst_contr = 0


   
    if k == 32:

        flag_syst_contr = 1
        
        


cv2.destroyAllWindows()