import cv2
import numpy as np
import argparse
import serial


def nothing(x):
    pass

cap = cv2.VideoCapture(0)





center_deviation = 5




cv2.createTrackbar('deviation','image', 180, 240, nothing)

x = None
y = None

while(1):


    x = None
    y = None



  



    if (x or y) is not None:
       
        if x > x_right_deviation or x < x_left_deviation or y < y_up_deviation or y >y_down_deviation:

            if x > x_right_deviation:
                print('deviation to the right x')

                value_PWM_first_serv = value_PWM_first_serv - 10

                if value_PWM_first_serv < 0:
                    print('low value first serv')    
                    value_PWM_first_serv = 0 

                else:                 
                    send_pkg = bytes([ord('#'), first_serv]) + value_PWM_first_serv.to_bytes(2, byteorder='big')
                    ser.write(send_pkg)

            if x < x_left_deviation:
                print('deviation to the left x')

      

                value_PWM_first_serv = value_PWM_first_serv + 10

                if value_PWM_first_serv > 1000:
                    print('great value second serv') 
                    value_PWM_first_serv = 1000
               
                else:
                    send_pkg = bytes([ord('#'), first_serv]) + value_PWM_first_serv.to_bytes(2, byteorder='big')
                    ser.write(send_pkg)


            if y < y_up_deviation:
                print('upward deviation y')
                
  

                value_PWM_second_serv = value_PWM_second_serv - 10
                if value_PWM_second_serv < 0:

                    print('low value second serv') 
                    value_PWM_second_serv = 0
                
                else:
                    send_pkg = bytes([ord('#'), second_serv]) + value_PWM_second_serv.to_bytes(2, byteorder='big')
                    ser.write(send_pkg)             

            if y > y_down_deviation:
 

                value_PWM_second_serv = value_PWM_second_serv + 10

                if value_PWM_second_serv > 1000:

                    print('great value of the second serv')
                    value_PWM_second_serv = 1000

                else:
                    send_pkg = bytes([ord('#'), second_serv]) + value_PWM_second_serv.to_bytes(2, byteorder='big')
                    ser.write(send_pkg)    

                print('downward deviation y')
        
        else: print('good')        
        

    else: print('not found x or y')



    

    




