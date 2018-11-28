#include <ch.h>
#include <hal.h>
#include <stdint.h>
#include <chprintf.h>

#define MIN_VALUE_US_PWM_2 750
#define MAX_VALUE_US_PWM_2 1850
#define STEP_FOR_SERVO_2 1.1

#define MIN_VALUE_US_PWM_1 750
#define MAX_VALUE_US_PWM_1 2200
#define STEP_FOR_SERVO_1 1.45
// -----------------------------------------
//
//    Equalizer API
//
// -----------------------------------------

struct Value_PWM
{

  uint8_t num_serv;
  uint16_t value_PWM;

};

struct Value_Serial
{
  uint8_t num_serv;
  uint16_t value_PWM;
};

PWMConfig pwmConf = {
    .frequency      = 1000000,  // 1MHz
    .period         = 10000,    // 10ms ~ 100Hz
    .callback       = NULL,
    .channels       = {
                          {.mode = PWM_OUTPUT_ACTIVE_HIGH, .callback = NULL},
                          {.mode = PWM_OUTPUT_DISABLED,    .callback = NULL},
                          {.mode = PWM_OUTPUT_DISABLED,    .callback = NULL},
                          {.mode = PWM_OUTPUT_DISABLED,    .callback = NULL}
                      },
    .cr2            = 0,
    .dier           = 0
};


PWMDriver *pwmDriver_serv_1 = &PWMD2;
PWMDriver *pwmDriver_serv_2 = &PWMD3;



static const SerialConfig sdcfg = {
  .speed = 115200,          /* baudrate, directly number */
  .cr1 = 0,               
  .cr2 = 0,                 
  .cr3 = 0                  
};

SerialDriver *interface_comm_dr = &SD2;

void interface_comm_init ( void )
{
    palSetPadMode( GPIOD, 5, PAL_MODE_ALTERNATE(7) );   // TX = PG_14
    palSetPadMode( GPIOD, 6, PAL_MODE_ALTERNATE(7) );   // RX = PG_9

    sdStart( interface_comm_dr, &sdcfg );
}

void interface_PWM_init()
{
  palSetPadMode( GPIOA, 5, PAL_MODE_ALTERNATE(1) );
  palSetPadMode( GPIOA, 6, PAL_MODE_ALTERNATE(2) );

  pwmStart( pwmDriver_serv_1 , &pwmConf );
  pwmStart( pwmDriver_serv_2 , &pwmConf );

  pwmDisableChannel(pwmDriver_serv_1, 0);
  pwmDisableChannel(pwmDriver_serv_2, 0);
}



void PWM_servo_1(uint16_t value_PWM)
{
  pwmEnableChannel(pwmDriver_serv_1, 0, value_PWM);
}

void PWM_servo_2(uint16_t value_PWM)
{
  pwmEnableChannel(pwmDriver_serv_2, 0, value_PWM);
}



uint16_t clip_servo(uint16_t value_PWM, uint16_t min, uint16_t max)
{
 value_PWM = (value_PWM  < min) ? min : value_PWM;
 value_PWM = (value_PWM  > max) ? max : value_PWM;
 return value_PWM;
}



void interface_servo(struct Value_PWM value)
{
  if(value.num_serv!=0)
  {
    if(value.num_serv==1)
    {

      value.value_PWM=MIN_VALUE_US_PWM_1 + value.value_PWM * STEP_FOR_SERVO_1;              // Get the actual PWM value

      value.value_PWM= clip_servo(value.value_PWM, MIN_VALUE_US_PWM_1, MAX_VALUE_US_PWM_1); // Check the value
      PWM_servo_1(value.value_PWM);

    }
    else if(value.num_serv==2)
    {
      value.value_PWM=MIN_VALUE_US_PWM_2 + value.value_PWM * STEP_FOR_SERVO_2;              // Get the actual PWM value

      value.value_PWM= clip_servo(value.value_PWM, MIN_VALUE_US_PWM_2, MAX_VALUE_US_PWM_2); // Check the value
      PWM_servo_2(value.value_PWM);

    }

  }

}


struct Value_Serial interface_comm_get_value ( void )
{

    struct Value_Serial result;
    char start_byte;
    uint8_t received_bytes[3];

    /*
     * Reset the value of the structure in the case of garbage
     */
    result.num_serv = 0;
    result.value_PWM = 0;

    msg_t msg = sdReadTimeout( &SD2, &start_byte, 1, MS2ST( 10 ) ); 

    if(msg==1)                      // Waiting for data
    {
      if(start_byte == '#')         // Expect starting byte
      {
        msg = sdReadTimeout( &SD2, &received_bytes, 3, MS2ST( 10 ) );

        if ( msg == 3 )             // Expect three bytes and write them to the structure
        {
            result.num_serv = received_bytes[0];
            result.value_PWM = (received_bytes[1]<<8)|(received_bytes[2]);

            return result;
        }
      }
    }
    return result;
}




int main(void)
{
    chSysInit();
    halInit(); 

    interface_comm_init();          // Initialization for Serial
    interface_PWM_init();           // Initialization for PWM
    struct Value_Serial accepted;   // Structure for receiving data from Serial
    struct Value_PWM value;         // The structure that is used to control PWM


    while (true)
    {

      accepted = interface_comm_get_value(); // Get the value from serial

      /*
       * re-value in structure
       */
      value.num_serv = accepted.num_serv;
      value.value_PWM = accepted.value_PWM;

      interface_servo(value);                // Change values ​​of PWM depending on the accepted values


    }
}
