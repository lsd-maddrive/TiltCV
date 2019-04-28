#ifndef COMMUNICATION_H_
#define COMMUNICATION_H_

#include <errno.h>
#include <stdint.h>

/*** Macroses ***/

/* Define "No error" code bacause there is no such code in errno.h */
#ifndef EOK
    #define EOK 0
#endif

/*** Types ***/

typedef struct
{
    uint8_t     num_serv;
    uint16_t    value_PWM;

} serial_comm_pkg_t;

/*** Protos ***/

/*
 * @brief   Communication module initialization
 */
void    serial_comm_init( void );

/*
 * @brief   Get package with new info
 * @param   p_pkg   Pointer to <serial_comm_pkg_t> structure
 * @return  EOK     New info is filled
 *          EINVAL  Invalid pointer
 *          EIO     Communication error
 *
 * @note    Blocking function with 10 ms timeout
 */
int     serial_comm_get_pkg( serial_comm_pkg_t *p_pkg );

#endif /* COMMUNICATION_H_ */
