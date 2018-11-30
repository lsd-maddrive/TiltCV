#ifndef TILT_UNIT_H_
#define TILT_UNIT_H_

#include <stdint.h>

/*** Macroses ***/

#define CLIP_VALUE(x, min, max) ( (x) < (min) ? (min) :     \
                                  (x) > (max) ? (max) : (x) )

/*** Types ***/

typedef struct
{
#define TILT_UNIT_SERVO_IDX_HORIZONTAL  1
#define TILT_UNIT_SERVO_IDX_VERTICAL    2
    uint8_t     servo_idx;

#define TILT_UNIT_INPUT_MIN_VALUE       0
#define TILT_UNIT_INPUT_MAX_VALUE       1000
    int16_t     input_value;

} tilt_unit_state_t;

/*** Protos ***/

/*
 * @brief   Tilt unit initialization
 */
void tilt_unit_init( void );

/*
 * @brief   Set horizontal position of camera
 * @params  new_state   Structure with new state info
 */
void tilt_unit_update_state( tilt_unit_state_t new_state );

#endif /* TILT_UNIT_H_ */
