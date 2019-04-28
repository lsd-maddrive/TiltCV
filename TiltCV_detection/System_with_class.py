import cv2
import numpy as np
import argparse
import time
import json
import serial

import skfuzzy as fuzz
from skfuzzy import control as System_fuzzy



class Work_with_file(object):
    ######################
    # To work with files #
    ######################


    def __init__(self):
        self.Params_file = None #

    def Load_params(self):
        if not self.Params_file:
            return None

        with open(self.Params_file, "r") as read_file:
            self.data = json.load(read_file)

    def Save_params(self):
        if not self.Params_file:
            return None

        with open(self.Params_file, "w") as write_file:
            json.dump(self.data, write_file)

class System_control_position(object):
   
    def __init__(self,data):
        try:
            self.Integrator_ratio = self.data["Integrator_ratio"]

            self.Task = self.data["Task"]

            self.extreme_border_membership_function = self.data["Extreme_border_membership_function"]
            self.middle_border_membership_function = self.data["Middle_border_membership_function"]
            
            self.Extreme_border_output_function = self.data["Extreme_border_output_function"]
            self.Middle_border_output_function = self.data["Middle_border_output_function"]

            ############################################################
            #      initialization of fuzzy logic system parameters     #
            ############################################################
            self.value_PWM_serv = self.System_fuzzy.Consequent(np.arange(-self.extreme_border_membership_function, self.extreme_border_membership_function+1, 1), 'membership_value_PWM')
            self.error = self.System_fuzzy.Antecedent(np.arange(-200, 201, 1), 'error')

            self.membership_value_PWM['low'] = self.fuzz.trapmf(self.membership_value_PWM.universe, [-self.extreme_border_membership_function,-self.extreme_border_membership_function, -self.middle_border_membership_function, 0])
            self.membership_value_PWM['medium'] = self.fuzz.trimf(self.membership_value_PWM.universe, [-self.middle_border_membership_function, 0, self.middle_border_membership_function])
            self.membership_value_PWM['high'] = self.fuzz.trapmf(self.membership_value_PWM.universe, [0, self.middle_border_membership_function ,self.extreme_border_membership_function ,self.extreme_border_membership_function])

            self.error['poor'] = self.fuzz.trapmf(self.error.universe, [-self.Extreme_border_output_function,-self.Extreme_border_output_function,-self.Middle_border_output_function, 0])
            self.error['zero'] = self.fuzz.trimf(self.error.universe, [-self.Middle_border_output_function, 0, self.Middle_border_output_function])
            self.error['good'] = self.fuzz.trapmf(self.error.universe, [0,self.Middle_border_output_function, self.Extreme_border_output_function, self.Extreme_border_output_function])

            self.rule1 = self.System_fuzzy.Rule(self.error['poor'], self.membership_value_PWM['low'])
            self.rule2 = self.System_fuzzy.Rule(self.error['zero'], self.membership_value_PWM['medium'])
            self.rule3 = self.System_fuzzy.Rule(self.error['good'], self.membership_value_PWM['high'])

            self.Rule_for_system = self.System_fuzzy.ControlSystem([self.rule1, self.rule2, self.rule3])
            self.Out_membership = self.System_fuzzy.ControlSystemSimulation(self.Rule_for_system)

        except KeyError:
            print('Sorry, no variables in file. System_control_position. System not initialized')
            break
      

    ######################################## 
    # the difference of the task and error #
    ########################################
    def Get_error(self):
        self.Delta = self.Task - self.Object_position

    #############################################################
    # the error value multiplied by the integrator coefficient  #
    #  is added to the current servo position                   #
    #############################################################
    def Integrator_system(self):
        self.Get_error()
        self.Servo_position = self.Servo_position + self.Delta * self.Integrator_ratio


    ###############################################
    # a fuzzy logic system output value is added  # 
    # to the current servo position               #
    ###############################################
    def Integrator_with_Fuzzy_coefficient(self):
        
        self.Get_error()

        self.Out_membership.input['error'] = self.Delta
        self.Out_membership.compute()

        self.Fuzzy_ratio = int(self.Out_membership.output['value_PWM_x_serv'])
        self.Servo_position = self.Servo_position + self.Fuzzy_ratio
        

class Work_with_frame(Work_with_file):

    def __init__(self):
        try:
            self.Params_file = 'Frame_setting.json'
            self.data =  self.Load_params()

            self.lower_value = self.data["Lower_value_for_HSV_boudrate"]
            self.upper_value = self.data["Upper_value_for_HSV_boudrate"]
            self.erosion_iter = self.data["Value_iteration_erosion"]
            self.dilation_iter = self.data["Value_iteration_dilation"]
            self.show_frame = self.data["Show_frame"]

            self.kernel = np.ones((3,3), np.uint8)
            self.cap = cv2.VideoCapture(0)

        except KeyError:
            print('Sorry, no variables in file. Work_with_frame')
            
    
    
    ##########################################################
    #   blur and convert to HSV format,                      #
    #   select the desired range of hsv                      #
    #   and use morphological operators to get rid of noise  # 
    ##########################################################  
    def image_processing(self, frame):
        
        self.blur = cv2.GaussianBlur(frame,(3,3),0)
        self.hsv = cv2.cvtColor(self.blur, cv2.COLOR_BGR2HSV)

        self.hsv_with_boundaries = cv2.inRange(self.hsv, self.lower_value, self.upper_value)

        self.erosion = cv2.erode(self.hsv_with_boundaries, self.kernel, iterations = self.erosion_iter)
        self.processed = cv2.dilate(self.erosion, self.kernel, iterations = self.dilation_iter)


    ##########################################################
    # finding the largest contour on the processed image,    #
    # obtaining the coordinates of the center of the contour #
    # and the largest deviation from the center as a radius  #
    ##########################################################
    def find_object(self):
        _, frame = self.cap.read()
        self.image_processing(frame)

        self.x = None
        self.y = None
        
        _, self.contours, hierarchy = cv2.findContours(self.processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if self.contours:
            cnt = max(self.contours, key = cv2.contourArea)
            (x,y), radius = cv2.minEnclosingCircle(cnt)

            self.x = int(self.x)
            self.y = int(self.y)
            
            
    #############################################
    # selection and display of the found object #
    #############################################
    def show_frame_with_object(self):
        
        if self.show_frame == 'y':   
            self.center = (int(self.x),int(self.y))	 
            self.radius = int(self.radius)
            cv2.circle(self.frame,self.center,self.radius,(0,255,0),2)
            cv2.imshow('image',self.frame)   

class Merge_system(Work_with_file,System_control_position):
    
    def __init__(self,name):
        Work_with_file.__init__(self)
        
        #########################################################
        # connect the file with the parameters and get the data #
        #########################################################
        try:
            self.Params_file = 'Setting_params_{}.json'.format(name)
            self.data = self.Load_params()
            
        except FileNotFoundError:
            print('oops, the\''+ self.Params_file + '\'file does not exist in this directory')
            
        System_control_position.__init__(self, self.data)


        ################################################################
        # adjust the serial and set the servo to the starting position #
        ################################################################         
        self.ser = serial.Serial('/dev/ttyUSB0',115200,timeout=1)
        self.Servo_position = self.data["Servo_position"]
        self.Number_serv = self.data["Number_serv"]
        self.Send_msg()


    ##########################
    # Sending a data package # 
    ##########################
    def Send_msg(self):
        self.send_pkg = bytes([ord('#'), self.Number_serv]) + self.Servo_position.to_bytes(2, byteorder='big')
        self.ser.write(self.send_pkg) 






Frame_work = Work_with_frame()

Control_system_x = Merge_system(x)

Control_system_y = Merge_system(y)

Frame_work.find_object()
Control_system_x.Object_position = Frame_work.x
Control_system_y.Object_position = Frame_work.y
