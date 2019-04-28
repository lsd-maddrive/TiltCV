#include <ch.h>
#include <hal.h>
#include <stdint.h>
#include <chprintf.h>

#include "communication.h"
#include "tilt_unit.h"

int main(void)
{
    chSysInit();
    halInit(); 

    serial_comm_pkg_t   input_pkg;  // Structure for receiving data from Serial
    serial_comm_init();             // Initialization for Serial

    tilt_unit_state_t   tilt_state;
    tilt_unit_init();               // Initialization for PWM

    while ( 1 )
    {
        int result = serial_comm_get_pkg( &input_pkg ); // Get the value from serial

        if ( result != EOK )
        {
            continue;
        }

        tilt_state.servo_idx    = input_pkg.num_serv;
        tilt_state.input_value  = input_pkg.value_PWM;

        tilt_unit_update_state( tilt_state );                // Change values of PWM depending on the accepted values
    }
}
