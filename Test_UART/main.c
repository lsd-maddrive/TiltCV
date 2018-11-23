#include <ch.h>
#include <hal.h>

#include <chprintf.h>

// -----------------------------------------
//
//    Equalizer API
//
// -----------------------------------------




PWMConfig pwmConf = {
    .frequency      = 1000000,  // 1MHz
    .period         = 10000,    // 10ms ~ 100Hz
    .callback       = NULL,
    .channels       = {
                           /* For all drivers channels 3 and 2 are used */
                          {.mode = PWM_OUTPUT_DISABLED,     .callback = NULL},
                          /* PWM_COMPLEMENTARY_OUTPUT_ACTIVE_LOW - because channel is TIM1_CH2N - complementary mode */
                          /* for this mode set STM32_PWM_USE_ADVANCED in mcuconf.h */
                          {.mode = PWM_OUTPUT_ACTIVE_HIGH | PWM_COMPLEMENTARY_OUTPUT_ACTIVE_LOW,  .callback = NULL},
                          {.mode = PWM_OUTPUT_ACTIVE_HIGH,  .callback = NULL},
                          {.mode = PWM_OUTPUT_DISABLED,     .callback = NULL}
                      },
    .cr2            = 0,
    .dier           = 0
};

PWMDriver *eq_dr_led1 = &PWMD3;
PWMDriver *eq_dr_led2 = &PWMD4;
PWMDriver *eq_dr_led3 = &PWMD1;

/* Each <eq_delta_value> new led starts */
static uint16_t eq_delta_value      = 80;
static float    eq_value_2_dc_rate  = 0;

struct Value_PWM
        {

            uint8_t num_serv;
            uint16_t value_PWM;

        };
/*
 * LED1 - B0    - T3C3
 * LED2 - B7    - T4C2
 * LED3 - B14   - T1C2N
 */
void led_equalizer_init ( void )
{
    eq_value_2_dc_rate = (float)pwmConf.period / eq_delta_value;

    palSetLineMode( LINE_LED1, PAL_MODE_ALTERNATE(2) );
    palSetLineMode( LINE_LED2, PAL_MODE_ALTERNATE(2) );
    palSetLineMode( LINE_LED3, PAL_MODE_ALTERNATE(1) );

    /* Just because configs are same - I can use one structure */
    pwmStart( eq_dr_led1, &pwmConf );
    pwmStart( eq_dr_led2, &pwmConf );
    pwmStart( eq_dr_led3, &pwmConf );
}

/* Static in proto means that function is not public */
/*
 * in:  <value> - input value from user
 *      <idx>   - number of LED in line
 */
static uint32_t equalizer_value_2_dc ( int32_t value, uint16_t idx )
{
    uint32_t duty_cycle = (value - eq_delta_value * idx) * eq_value_2_dc_rate;
    return ( duty_cycle > pwmConf.period ? pwmConf.period : duty_cycle );
}

/*
 * @note: <value> can be in range [0; <eq_delta_value> * 3]
 */
void led_equalizer_set_value ( uint16_t value )
{
    uint32_t led1_dc = equalizer_value_2_dc( value, 0 );
    uint32_t led2_dc = equalizer_value_2_dc( value, 1 );
    uint32_t led3_dc = equalizer_value_2_dc( value, 2 );

    pwmEnableChannel( eq_dr_led1, 2, led1_dc );
    pwmEnableChannel( eq_dr_led2, 1, led2_dc );
    pwmEnableChannel( eq_dr_led3, 1, led3_dc );
}


// -----------------------------------------
//
//    Interface API
//
// -----------------------------------------

/*
 * Serial configuration
 */
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

    msg = sdReadTimeout( &SD2, start_byte, 1, MS2ST( 10 ) );

    if(start_byte == '#')
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


/*
 * Test transfer
 */



// -----------------------------------------
//
//    Main application
//
// -----------------------------------------

/* Test case - equalizer works in full range */
//#define TEST_CASE

int main(void)
{
    struct Value_PWM;
    chSysInit();
    halInit();

    interface_comm_init();
    led_equalizer_init();

    while (true)
    {
#ifdef TEST_CASE

        static uint16_t cntr = 0;

        led_equalizer_set_value( cntr++ );
        cntr = cntr >= 240 ? 0 : cntr;

#else // TEST_CASE

        int16_t new_value = interface_comm_get_value();
        if ( new_value > 0 )
        {
            /* Here we get new value */
            led_equalizer_set_value( new_value );
        }

#endif // TEST_CASE

        chThdSleepMilliseconds( 10 );
    }
}
