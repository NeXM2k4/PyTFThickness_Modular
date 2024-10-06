import serial

# Configure the serial connection
ser = serial.Serial(port="/dev/ttyACM0", parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE) #, timeout=1

# Open a file on your computer to write the received data
destination_file = open("./store_info.txt", "w")

# Read and write data until the transfer is complete
while True:
	pico_cmd_bytes=ser.read(3)
	pico_cmd_read=pico_cmd_bytes.decode("ascii")
	print(pico_cmd_read)
	destination_file.write(pico_cmd_read)

# Close the files and serial connection
destination_file.close()
serial_connection.close()
