#include "communication.h"

#include <hal.h>

static const SerialConfig sdcfg = {
  .speed = 115200,          /* baudrate, directly number */
  .cr1 = 0,
  .cr2 = 0,
  .cr3 = 0
};

SerialDriver *comm_dr = &SD2;

/*
 * @brief   Communication module initialization
 */
void serial_comm_init( void )
{
    palSetPadMode( GPIOD, 5, PAL_MODE_ALTERNATE(7) );   // TX = PD_5
    palSetPadMode( GPIOD, 6, PAL_MODE_ALTERNATE(7) );   // RX = PD_6

    sdStart( comm_dr, &sdcfg );
}

/*
 * @brief   Get package with new info
 * @param   p_pkg   Pointer to <serial_comm_pkg_t> structure
 * @return  EOK     New info is filled
 *          EINVAL  Invalid pointer
 *          EIO     Communication error
 *
 * @note    Blocking function with 10 ms timeout
 */
int serial_comm_get_pkg( serial_comm_pkg_t *p_pkg )
{
    if ( p_pkg == NULL )
        return EINVAL;

    msg_t msg = sdGetTimeout( comm_dr, MS2ST( 10 ) );
    if ( msg < 0 )
    {
        return EIO;
    }

    char start_byte = msg;
    if ( start_byte == '#' )         // Expect starting byte
    {
        /* TODO << Bad thing, because we can`t give structure to fill, BigEndian =( */
        uint8_t rcv_buffer[3];
        int32_t rcv_bytes = sizeof( rcv_buffer );

        msg = sdReadTimeout( comm_dr, rcv_buffer, rcv_bytes, MS2ST( 10 ) );
        if ( msg != rcv_bytes )             // Expect three bytes and write them to the structure
        {
            return EIO;
        }

        /* Just in future replace it with structure fill automatically */
        p_pkg->num_serv  = rcv_buffer[0];
        p_pkg->value_PWM = (rcv_buffer[1]<<8)|(rcv_buffer[2]);
    }

    return EOK;
}


