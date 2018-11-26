#include <ch.h>
#include <hal.h>
#include <stdint.h>
#include <chprintf.h>

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
                           /* For all drivers channels 3 and 2 are used */
                          {.mode = PWM_OUTPUT_ACTIVE_HIGH,     .callback = NULL},
                          /* PWM_COMPLEMENTARY_OUTPUT_ACTIVE_LOW - because channel is TIM1_CH2N - complementary mode */
                          /* for this mode set STM32_PWM_USE_ADVANCED in mcuconf.h */
                          {.mode = PWM_OUTPUT_DISABLED,  .callback = NULL},
                          {.mode = PWM_OUTPUT_DISABLED,  .callback = NULL},
                          {.mode = PWM_OUTPUT_DISABLED,  .callback = NULL}
                      },
    .cr2            = 0,
    .dier           = 0
};

PWMDriver *pwmDriver_serv_1 = &PWMD2;
PWMDriver *pwmDriver_serv_2 = &PWMD3;



static const SerialConfig sdcfg = {
  .speed = 115200,          /* baudrate, directly number */
  .cr1 = 0,                 /* CR1 register, no need to set this */
  .cr2 = 0,                 /* CR2 register, no need to set this */
  /* RM says that USART_CR2_LINEN enables error detection,
     so this should work without this USART_CR2_LINEN */
  .cr3 = 0                  /* CR3 register, no need to set this */
  /*
   * if need to set one of registers use USART_CR1_*, USART_CR2_* or USART_CR3_*
   */
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

    //msg_t msg = sdReadTimeout( &SD2, start_byte, 1, MS2ST( 10 ) );
    msg_t msg = sdGetTimeout( &SD2, MS2ST( 10 ) );
    start_byte = msg;
    //if(start_byte == '#')
      if(start_byte == 1)
    {

         msg = sdReadTimeout( &SD2, received_bytes, 3, MS2ST( 10 ) );

        if ( msg == 3 )
        {

            result.num_serv = received_bytes[0];
            result.value_PWM = (received_bytes[1]<<8)|(received_bytes[2]);
            return result;
        }
    }

    return result;
}


int main(void)
{
    struct Value_PWM result;
    palSetLine(LINE_LED2);
    // need palSetPadMode for PWM pin;
    palSetPadMode( GPIOA, 5, PAL_MODE_ALTERNATE(1) );
    palSetPadMode( GPIOA, 6, PAL_MODE_ALTERNATE(2) );


    interface_comm_init();
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
        chThdSleepMilliseconds( 10 );
    }
}
