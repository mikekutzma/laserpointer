import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM0',9600)
try:
    while True:
        print(ser.readline())
        sleep(.1)
finally:
    ser.close()

