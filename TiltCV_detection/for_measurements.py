import numpy as np


def measurements(time, x_real, y_real, x_center, y_center):
   
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

                
                
                x_control_syst, y_control_syst,time_control_syst = cs.write_value_error(x_error,y_error,x_control_syst, y_control_syst, start_time,time_control_syst)

                if max(time_control_syst)  > 100:

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