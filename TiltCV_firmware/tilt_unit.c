#include "tilt_unit.h"

#include <hal.h>

static void tilt_unit_set_horizontal_pos( int16_t pos_val );
static void tilt_unit_set_vertical_pos( int16_t pos_val );

#define SERVO_VRT_MIN_VALUE_US      750
#define SERVO_VRT_MAX_VALUE_US      1850
#define SERVO_VRT_INPUT_2_US(x)     ((x) * 1.1 + SERVO_VRT_MIN_VALUE_US)

#define SERVO_HRZ_MIN_VALUE_US      750
#define SERVO_HRZ_MAX_VALUE_US      2200
#define SERVO_HRZ_INPUT_2_US(x)     ((x) * 1.45 + SERVO_HRZ_MIN_VALUE_US)

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

PWMDriver *pwm_hrz_dr = &PWMD2;
PWMDriver *pwm_vrt_dr = &PWMD3;

/*
 * @brief   Tilt unit initialization
 */
void tilt_unit_init( void )
{
    palSetPadMode( GPIOA, 5, PAL_MODE_ALTERNATE(1) );
    palSetPadMode( GPIOA, 6, PAL_MODE_ALTERNATE(2) );

    pwmStart( pwm_hrz_dr , &pwmConf );
    pwmStart( pwm_vrt_dr , &pwmConf );

    pwmDisableChannel( pwm_hrz_dr, 0 );
    pwmDisableChannel( pwm_vrt_dr, 0 );
}

/*
 * @brief   Set horizontal position of camera
 * @params  new_state   Structure with new state info
 */
void tilt_unit_update_state( tilt_unit_state_t new_state )
{
    if ( new_state.servo_idx == TILT_UNIT_SERVO_IDX_HORIZONTAL )
    {
        tilt_unit_set_horizontal_pos( new_state.input_value );
    }
    else if ( new_state.servo_idx == TILT_UNIT_SERVO_IDX_VERTICAL )
    {
        tilt_unit_set_vertical_pos( new_state.input_value );
    }
}

static void tilt_unit_set_horizontal_pos( int16_t pos_val )
{
    pos_val = CLIP_VALUE( pos_val, TILT_UNIT_INPUT_MIN_VALUE, TILT_UNIT_INPUT_MAX_VALUE );

    uint32_t pwm_us_value = SERVO_HRZ_INPUT_2_US( pos_val );
    pwm_us_value = CLIP_VALUE( pwm_us_value, SERVO_HRZ_MIN_VALUE_US, SERVO_HRZ_MAX_VALUE_US );

    pwmEnableChannel( pwm_vrt_dr, 0, pwm_us_value );
}

static void tilt_unit_set_vertical_pos( int16_t pos_val )
{
    pos_val = CLIP_VALUE( pos_val, TILT_UNIT_INPUT_MIN_VALUE, TILT_UNIT_INPUT_MAX_VALUE );

    uint32_t pwm_us_value = SERVO_VRT_INPUT_2_US( pos_val );
    pwm_us_value = CLIP_VALUE( pwm_us_value, SERVO_VRT_MIN_VALUE_US, SERVO_VRT_MAX_VALUE_US );

    pwmEnableChannel( pwm_hrz_dr, 0, pwm_us_value );
}
