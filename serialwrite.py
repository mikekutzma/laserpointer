import serial
from time import sleep
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--writetype', '-wt', default='deg', type=str)
args = parser.parse_args()

writemap = {
    'deg': 'Degree',
    'micro': 'Microsecond',
}

ser = serial.Serial('/dev/ttyACM0', 9600)
print('Enter positions')
try:
    while True:
        x, y = (str(a) for a in input().strip().split(','))
        print(x, y)
        serstr = "<{},{},{}>".format(writemap[args.writetype], x, y)
        ser.write(serstr.encode('utf-8'))
        ser.flush()
        print(serstr)
        sleep(.1)
finally:
    ser.close()
