#include <ch.h>
#include <hal.h>

#include <chprintf.h>

static THD_WORKING_AREA(waThread, 128);
static THD_FUNCTION(Thread, arg) 
{
    arg = arg;

    while (true)
    {
        chThdSleepSeconds(1);
    }
}

static const I2CConfig i2ccnfg = {
                                  .op_mode = OPMODE_I2C,
                                  .clock_speed = 400000,
                                  .duty_cycle = FAST_DUTY_CYCLE_2,
};

I2CDriver *imu_bus = &I2CD1;


int main(void)
{
    /* RT Core initialization */
    chSysInit();
    /* HAL (Hardware Abstraction Layer) initialization */
    halInit();

    chThdCreateStatic(waThread, sizeof(waThread), NORMALPRIO, Thread, NULL /* arg is NULL */);

    palSetPadMode( GPIOB, 6, PAL_MODE_STM32_ALTERNATE_OPENDRAIN );
    palSetPadMode( GPIOB, 7, PAL_MODE_STM32_ALTERNATE_OPENDRAIN );



    while (true)
    {   i2cStart(imu_bus,&i2ccnfg);
        chThdSleepSeconds(1);
        i2cStop(imu_bus);
    }
}
