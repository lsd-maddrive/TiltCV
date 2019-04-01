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
import plot_graph as pg



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

PWM_output_limit, PWM_MF_change_value_1, high_value_fuzzy, medium_value_fuzzy = tb.getFuzzy()

fuzzy_syst_for_y = cs.fuzzy_control_init_for_y(30, 16, 200, 150)
fuzzy_syst_for_x = cs.fuzzy_control_init_for_x(20, 13, 200, 120)

count = 0
time_control_system_measurements =0
time_system_control = 0
flag_new_measurements = 1

while(1):

    _, frame = cap.read()
    output = frame.copy()

    output,x_real,y_real = fo.finding_a_circle_around_the_contour(frame)

    dilation = ip.processing_morphological_operators(frame)
    
    if flag_start_system_control == 1:
    	
        if time_control_system_measurements > 1:
            
            if x_real or y_real is not None:

                if flag_new_measurements == 1:
                    
                    flag_new_measurements =0
                    time_control_syst, x_control_syst, y_control_syst = pg.clear_data(time_control_syst,x_control_syst,y_control_syst)
                    start_time = time.time()


                x_error = x_center - x_real
                y_error = y_center - y_real

                value_PWM_first_serv, value_PWM_second_serv = cs.check_deviation(x_real,y_real,value_PWM_first_serv,value_PWM_second_serv,ser)
                # x_control_syst, y_control_syst,time_control_syst = cs.write_value_error(x_real,y_real,x_control_syst, y_control_syst, start_time,time_control_syst)
                
                # value_PWM_first_serv = cs.fuzzy_control_get_output_for_x(fuzzy_syst_for_x,x_error,value_PWM_first_serv,ser)
                # value_PWM_second_serv = cs.fuzzy_control_get_output_for_y(fuzzy_syst_for_y, y_error, value_PWM_second_serv, ser)
                
                
                x_control_syst, y_control_syst,time_control_syst = cs.write_value_error(x_error,y_error,x_control_syst, y_control_syst, start_time,time_control_syst)

                if max(time_control_syst)  > 1.5:

                    time_control_syst_reserv.append(time_control_syst)
                    x_control_syst_reserv.append(x_control_syst)
                    y_control_syst_reserv.append(y_control_syst)

                    count = count + 1

                    value_PWM_first_serv = 500
                    value_PWM_second_serv = 500

                    sc.SendPkg(1,value_PWM_first_serv,ser)
                    sc.SendPkg(2,value_PWM_second_serv,ser)
                     
                    flag_new_measurements = 1
                    time_control_system_measurements = 0
                    start_time_system_control = time.time()

                    if count > number_of_measurements:
                        pg.write_to_mat(time_control_syst_reserv,x_control_syst_reserv,y_control_syst_reserv)
                        flag_start_system_control = 0
                        pg.plot_graph(time_control_syst_reserv,x_control_syst_reserv,y_control_syst_reserv)
                        count=0
                    

        else:
            time_control_system_measurements = time.time() - start_time_system_control

    
    cv2.imshow('image',output)

    cv2.imshow('dilation', dilation)
    
    k = cv2.waitKey(5) & 0xFF
    
    if k == 27:
        
        break

    if k == 13:

        flag_start_system_control = 1
        start_time = time.time()

        # PWM_output_limit, PWM_MF_change_value_1, high_value_fuzzy, medium_value_fuzzy = tb.getFuzzy()
        # fuzzy_syst_for_x = cs.fuzzy_control_init_for_x(PWM_output_limit, PWM_MF_change_value_1, high_value_fuzzy, medium_value_fuzzy)

        start_time_system_control = time.time()
        
        number_of_measurements = tb.getValue_number_of_measurements()


   
    if k == 32:

        flag_start_system_control = 0
        
        time_control_syst, x_control_syst, y_control_syst = pg.clear_data(time_control_syst,x_control_syst,y_control_syst)
        time_control_syst_reserv, x_control_syst_reserv, y_control_syst_reserv = pg.clear_data(time_control_syst_reserv, x_control_syst_reserv, y_control_syst_reserv)


cv2.destroyAllWindows()