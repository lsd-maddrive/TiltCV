import track_bar as tb
import math
import serial_connection as sc
import cv2



def check_deviation_sign(x_real,y_real,value_PWM_first_serv,value_PWM_second_serv,ser):
   
    deviation = tb.getValueDeviation()

    coef =10
    x_center = 320
    y_center = 240


    
    if x_real or y_real is not None:

        x_deviation = abs(x_center - x_real)
        y_deviation = abs(y_center - y_real)

        if(x_deviation > deviation):
            value_PWM_first_serv = value_PWM_first_serv + math.copysign(1,x_center - x_real)*coef
            if(value_PWM_first_serv < 0):
                value_PWM_first_serv = 0

            if(value_PWM_first_serv> 1000):
                value_PWM_first_serv = 1000
            sc.SendPkg(1,int(value_PWM_first_serv),ser)


        if(y_deviation > deviation):
            value_PWM_second_serv = value_PWM_second_serv - math.copysign(1,y_center - y_real)*coef
            if(value_PWM_second_serv<0):
                value_PWM_second_serv = 0

            if(value_PWM_second_serv>1000):
                value_PWM_second_serv=1000
            sc.SendPkg(2,int(value_PWM_second_serv),ser)

    return value_PWM_first_serv, value_PWM_second_serv




def check_deviation(x_real,y_real,value_PWM_first_serv,value_PWM_second_serv,ser):
   
    deviation = tb.getValueDeviation()

    coef =0.1
    x_center = 320
    y_center = 240


    
    if x_real or y_real is not None:

        x_deviation = abs(x_center - x_real)
        y_deviation = abs(y_center - y_real)

        if(x_deviation > deviation):
            value_PWM_first_serv = value_PWM_first_serv + (x_center - x_real)*coef
            if(value_PWM_first_serv < 0):
                value_PWM_first_serv = 0

            if(value_PWM_first_serv> 1000):
                value_PWM_first_serv = 1000
            sc.SendPkg(1,int(value_PWM_first_serv),ser)


        if(y_deviation > deviation):
            value_PWM_second_serv = value_PWM_second_serv - (y_center - y_real)*coef
            if(value_PWM_second_serv<0):
                value_PWM_second_serv = 0

            if(value_PWM_second_serv>1000):
                value_PWM_second_serv=1000
            sc.SendPkg(2,int(value_PWM_second_serv),ser)

    return value_PWM_first_serv, value_PWM_second_serv
