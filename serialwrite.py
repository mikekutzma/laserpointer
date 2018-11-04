import pyautogui as pag
import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM1',9600)
print(ser.readline())
ser.write(b'5')
ser.flush()
print(ser.readline())
ser.write(b'100')
print(ser.readline())
sleep(.1)
ser.close()
