#include <ch.h>
#include <hal.h>
#include <stdint.h>
#include <chprintf.h>

#define Min_value_us_PWM_2 750;
#define Max_value_us_PWM_2 1850;

#define Min_value_us_PWM_1 750;
#define Max_value_us_PWM_1 2200;
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



/* Each <eq_delta_value> new led starts */
static uint16_t eq_delta_value      = 80;
static float    eq_value_2_dc_rate  = 0;


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


struct Value_PWM interface_comm_get_value ( void )
{

    struct Value_PWM result;
    char start_byte;
    uint8_t received_bytes[3];
    result.num_serv = 0;
    result.value_PWM = 0;

    msg_t msg = sdReadTimeout( &SD2, &start_byte, 1, MS2ST( 10 ) ); 

    if(msg==1)
    {
      if(start_byte == '#')
      {

        palToggleLine(LINE_LED2);
        msg = sdReadTimeout( &SD2, &received_bytes, 3, MS2ST( 10 ) );

        if ( msg == 3 )
        {
          palToggleLine(LINE_LED1);
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

    interface_comm_init(); 

    struct Value_PWM result;

    // Need function
    palSetPadMode( GPIOA, 5, PAL_MODE_ALTERNATE(1) );
    palSetPadMode( GPIOA, 6, PAL_MODE_ALTERNATE(2) );

    pwmStart( pwmDriver_serv_1 , &pwmConf );
    pwmStart( pwmDriver_serv_2 , &pwmConf );

    pwmDisableChannel(pwmDriver_serv_1, 0);
    pwmDisableChannel(pwmDriver_serv_2, 0);

    while (true)
    {

      result = interface_comm_get_value();

      if(result.num_serv != 0)
      {

        if(result.num_serv == 1)
        {
          pwmEnableChannel(pwmDriver_serv_1, 0, result.value_PWM);
        }

        else
        {
          pwmEnableChannel(pwmDriver_serv_2, 0, result.value_PWM);
        }

      }
    }
}
