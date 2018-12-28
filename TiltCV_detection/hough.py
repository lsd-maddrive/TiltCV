    if (x or y) is not None:
       
        if x > x_up_deviation or x < x_down_deviation or y < y_up_deviation or y >y_down_deviation:

            if x > x_up_deviation:
                print('deviation to the right x')
            
            if x < x_down_deviation:
                print('deviation to the left x')

            if y < y_up_deviation:
                print('upward deviation y')
            
            if y > y_down_deviation:
                print('downward deviation y')
        
        else: print('good')        
        

    else: print('not found x or y')