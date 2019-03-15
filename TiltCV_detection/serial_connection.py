
def InitSerial():
    ser = serial.Serial('/dev/ttyUSB0',115200,timeout=1)

    first_serv = 1
    second_serv = 2

    value_PWM_first_serv = 500
    value_PWM_second_serv = 500

    send_pkg = bytes([ord('#'), first_serv]) + value_PWM_first_serv.to_bytes(2, byteorder='big')
    ser.write(send_pkg)

    send_pkg = bytes([ord('#'), second_serv]) + value_PWM_second_serv.to_bytes(2, byteorder='big')
    ser.write(send_pkg)

    x_center = 320
    y_center = 240


def SendPkg(number_serv, value_PWM):
    
    send_pkg = bytes([ord('#'), number_serv]) + value_PWM.to_bytes(2, byteorder='big')
    ser.write(send_pkg) 