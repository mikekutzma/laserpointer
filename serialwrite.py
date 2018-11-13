import pyautogui as pag
import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM0',9600)
print('Enter positions')
try:
    while True:
        x = input()
        ser.write(x.strip().encode('utf-8'))
        ser.flush()
        sleep(.1)
finally:
    ser.close()
