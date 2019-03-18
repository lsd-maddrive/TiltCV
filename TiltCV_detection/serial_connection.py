import serial


def InitSerial(start_value_PWM_first_serv, start_value_PWM_second_serv):
	ser = serial.Serial('/dev/ttyUSB0',115200,timeout=1)

	first_serv = 1
	second_serv = 2

	SendPkg(first_serv,start_value_PWM_first_serv,ser)
	SendPkg(second_serv,start_value_PWM_second_serv,ser)

	return ser


def SendPkg(number_serv, value_PWM,ser):
	
	send_pkg = bytes([ord('#'), number_serv]) + value_PWM.to_bytes(2, byteorder='big')
	ser.write(send_pkg) 