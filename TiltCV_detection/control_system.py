import track_bar as tb
import math
import serial_connection as sc
import cv2
import time

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt



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

    coef =0.08
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


def write_value_error(x, y, x_control_syst, y_control_syst, start_time, time_control_syst):
    
    time_control_syst.append(time.time()-start_time)
    x_control_syst.append(x)
    y_control_syst.append(y)

    return x_control_syst, y_control_syst, time_control_syst




def fuzzy_control_init_for_x(PWM_output_limit,PWM_MF_change_value_1,high_value,medium_value):
    


    value_PWM_x_serv = ctrl.Consequent(np.arange(-PWM_output_limit, PWM_output_limit+1, 1), 'value_PWM_x_serv')

    x_error = ctrl.Antecedent(np.arange(-200, 201, 1), 'x_error')

    value_PWM_x_serv['low'] = fuzz.trapmf(value_PWM_x_serv.universe, [-PWM_output_limit,-PWM_output_limit, -PWM_MF_change_value_1, 0])
    value_PWM_x_serv['medium'] = fuzz.trimf(value_PWM_x_serv.universe, [-PWM_MF_change_value_1, 0, PWM_MF_change_value_1])
    value_PWM_x_serv['high'] = fuzz.trapmf(value_PWM_x_serv.universe, [0, PWM_MF_change_value_1 ,PWM_output_limit ,PWM_output_limit])



    x_error['poor'] = fuzz.trapmf(x_error.universe, [-high_value,-high_value,-medium_value, 0])
    x_error['zero'] = fuzz.trimf(x_error.universe, [-medium_value, 0, medium_value])
    x_error['good'] = fuzz.trapmf(x_error.universe, [0,medium_value,high_value,high_value])

    rule1_for_x = ctrl.Rule(x_error['poor'], value_PWM_x_serv['low'])
    rule2_for_x = ctrl.Rule(x_error['zero'], value_PWM_x_serv['medium'])
    rule3_for_x = ctrl.Rule(x_error['good'], value_PWM_x_serv['high'])

    value_x_ctrl = ctrl.ControlSystem([rule1_for_x, rule2_for_x, rule3_for_x])

    ctrl_x = ctrl.ControlSystemSimulation(value_x_ctrl)

    return ctrl_x


def fuzzy_control_init_for_y(PWM_output_limit,PWM_MF_change_value_1,high_value,medium_value):
    

    value_PWM_y_serv = ctrl.Consequent(np.arange(-PWM_output_limit, PWM_output_limit+1, 1), 'value_PWM_y_serv')

    y_error = ctrl.Antecedent(np.arange(-200, 201, 1), 'y_error')

    value_PWM_y_serv['low'] = fuzz.trapmf(value_PWM_y_serv.universe, [-PWM_output_limit,-PWM_output_limit, -PWM_MF_change_value_1, 0])
    value_PWM_y_serv['medium'] = fuzz.trimf(value_PWM_y_serv.universe, [-PWM_MF_change_value_1, 0, PWM_MF_change_value_1])
    value_PWM_y_serv['high'] = fuzz.trapmf(value_PWM_y_serv.universe, [0, PWM_MF_change_value_1 ,PWM_output_limit ,PWM_output_limit])



    y_error['poor'] = fuzz.trapmf(y_error.universe, [-high_value,-high_value,-medium_value, 0])
    y_error['zero'] = fuzz.trimf(y_error.universe, [-medium_value, 0, medium_value])
    y_error['good'] = fuzz.trapmf(y_error.universe, [0,medium_value,high_value,high_value])

    rule1_for_y = ctrl.Rule(y_error['poor'], value_PWM_y_serv['low'])
    rule2_for_y = ctrl.Rule(y_error['zero'], value_PWM_y_serv['medium'])
    rule3_for_y = ctrl.Rule(y_error['good'], value_PWM_y_serv['high'])

    value_y_ctrl = ctrl.ControlSystem([rule1_for_y, rule2_for_y, rule3_for_y])

    ctrl_y = ctrl.ControlSystemSimulation(value_y_ctrl)

    return ctrl_y






def fuzzy_control_get_output_for_x(fuzzy_syst, x_error, in_PWM, drive_serv):
    
    num_serv = 1
    fuzzy_syst.input['x_error'] = x_error
    fuzzy_syst.compute()

    value_PWM = int(fuzzy_syst.output['value_PWM_x_serv'])
    return put_PWM(in_PWM, value_PWM, num_serv, drive_serv)




def fuzzy_control_get_output_for_y(fuzzy_syst, y_error, in_PWM, drive_serv):
    
    num_serv = 2
    fuzzy_syst.input['y_error'] = y_error
    fuzzy_syst.compute()

    value_PWM = int(fuzzy_syst.output['value_PWM_y_serv'])
    return put_PWM(in_PWM, value_PWM, num_serv, drive_serv)




def put_PWM(in_PWM, value_PWM, num_serv, drive_serv):

    if num_serv == 1:
        out_PWM = in_PWM + value_PWM

    else:
        out_PWM = in_PWM - value_PWM

    if out_PWM > 1000:
        out_PWM = 1000

    if out_PWM < 0:
        out_PWM = 0

    sc.SendPkg(num_serv,int(out_PWM),drive_serv)

    return out_PWM