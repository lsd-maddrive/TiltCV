#include <ch.h>
#include <hal.h>

#include <chprintf.h>

/*
 * Setup:
 * halconf.h -  Enable HAL_USE_SERIAL
 *              To change the size of the buffer, change SERIAL_BUFFERS_SIZE
 * mcuconf.h -  Choose required serial STM32_SERIAL_USE_*
 */

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

#define SERIAL_CHARACTER            0x00
#define SERIAL_BYTE_ARRAY           0x01
#define SERIAL_UINT32               0x02
#define SERIAL_STRING               0x03
#define SERIAL_FORMATTED_STRING     0x04
#define SERIAL_MATLAB               0x05

//const uint8_t send_type = SERIAL_CHARACTER;
//const uint8_t send_type = SERIAL_BYTE_ARRAY;
//const uint8_t send_type = SERIAL_UINT32 ;
//const uint8_t send_type = SERIAL_STRING ;
//const uint8_t send_type = SERIAL_FORMATTED_STRING;
const uint8_t send_type = SERIAL_MATLAB;

int Flagfor2byte = 0; // flag to write two bytes

// need to fix
int16_t byte2;
int8_t byte1;

static THD_WORKING_AREA(waSender, 128);
static THD_FUNCTION(Sender, arg)
{
    arg = arg;      /* just to avoid warnings from compiler */
    while (true)
    {
      /* Read one byte data with timeout 10 ms */
                      msg_t msg = sdGetTimeout( &SD2, MS2ST( 10 ) );

                      if ( msg >= 0 )
                      {

                        if(Flagfor2byte == 0)
                        {
                          byte1 = msg;
                          Flagfor2byte = 1;

                        }

                        // merge two bytes
                        else
                        {
                          byte2 =( byte1 << 8 )| msg;
                          Flagfor2byte = 0;

                        }



                          if ( byte2 < 250 )
                          {
                            palClearLine(LINE_LED1);
                            palClearLine( LINE_LED2 );
                            palClearLine(LINE_LED3);

                          }

                          else if ( byte2 >= 250 && byte2 < 500 )
                          {
                            palSetLine(LINE_LED1);
                            palClearLine(LINE_LED2);
                            palClearLine(LINE_LED3);



                          }
                          else if (byte2 >= 500 && byte2 < 750)
                          {
                            palSetLine(LINE_LED1);
                            palSetLine(LINE_LED2);
                            palClearLine(LINE_LED3);


                          }
                          else
                          {
                            palSetLine(LINE_LED1);
                            palSetLine(LINE_LED2);
                            palSetLine(LINE_LED3);


                          }
                     // }
                      }
    }
}

int main(void)
{
    chSysInit();
    halInit();

    /* as 6th driver is used, use SD6 structure for driver functions */
    sdStart( &SD2, &sdcfg );
    /*
     * https://os.mbed.com/platforms/ST-Nucleo-F767ZI/
     * serial 6th driver is on PG_14, PG_9
     * alternate function is 8th (check datasheet)
     */
    palSetPadMode( GPIOD, 5, PAL_MODE_ALTERNATE(7) );  // TX = PG_14
    palSetPadMode( GPIOD, 6, PAL_MODE_ALTERNATE(7) );   // RX = PG_9

    /* create thread that sends just string */
    chThdCreateStatic( waSender, sizeof(waSender), NORMALPRIO, Sender, NULL );
    while (true)
    {
        chThdSleepSeconds( 1 );
       // get_external_value();


    }
}

