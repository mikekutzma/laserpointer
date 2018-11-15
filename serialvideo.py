from collections import deque
import cv2
from math import sqrt
import serial
import logging
import sys
import argparse


def square_root_weighted(result, x, i, n):
    if n < 1:
        return 0
    m = sqrt(n)
    factor = m * (n - (2 * m * m + 3 * m - 5) / 6)
    return result + x * sqrt(i) / factor


def linear_weighted(result, x, i, n):
    if n < 1:
        return 0
    factor = n * (n + 1) / 2.0
    return result + x * i / factor


def uniform_weighted(result, x, _, n):
    if n < 1:
        return 0
    return result + x / n


class FacePos:
    funcmap = {
        'linear': linear_weighted,
        'uniform': uniform_weighted,
        'sqrt': square_root_weighted,
    }
    writemap = {
        'deg': 'Degree',
        'micro': 'Microsecond',
    }

    def __init__(self, ser=None, logger=None, memory=10, weight_str='uniform', startpos=(80, 80), writetype='deg'):
        self.ser = ser
        self._logger = logger
        self.pos = (80, 80)
        self.q = deque([], maxlen=memory)
        self.weight_func = self.funcmap.get(weight_str, uniform_weighted)
        self.current_pos = startpos
        self.writetype = writetype

    def update(self, px, py):
        """
        We append right here so that we can use higher index -> higher weight.
        This can be done even with appending left, but it's a deque so why not.
        """
        self.q.append((px, py))
        if self._logger is not None:
            self._logger.debug('Queue updated with {},{}'.format(px, py))

    def posfunc(self):
        px, py = 0, 0
        for i, (x, y) in enumerate(self.q):
            px = self.weight_func(px, x, i + 1, len(self.q))
            py = self.weight_func(py, y, i + 1, len(self.q))

        return self.transform(px, py)

    def transform(self, x, y):
        if self.writetype == 'deg':
            px = 0.0666 * x + 59.3
            py = -0.06015 * y + 102.015
        elif self.writetype == 'micro':
            px = x
            py = y
        else:
            px = x
            py = y

        return px, py

    def write(self, thresh=1):
        px, py = self.posfunc()
        if _logger is not None:
            _logger.debug('PosFunc returned {},{}'.format(px, py))
        cx, cy = self.current_pos
        if sqrt((cx - px) ** 2 + (cy - py) ** 2) >= thresh:
            self.current_pos = (px, py)
            self._swrite()

    def _swrite(self):
        x, y = self.current_pos
        ser_str = '<' + self.writemap[self.writetype] + ',' + str(int(x)) + ',' + str(int(y)) + '>'
        if self.ser is not None:
            self.ser.write(ser_str.encode('utf-8'))
            self.ser.flush()
        if self._logger is not None:
            self._logger.info('Wrote {} to serial'.format(ser_str))


if __name__ == '__main__':

    face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('data/haarcascade_eye.xml')
    cap = cv2.VideoCapture(0)

    parser = argparse.ArgumentParser()
    parser.add_argument('--serial', action='store_true')
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--weights', '-w', default='uniform', type=str)
    parser.add_argument('--memory', '-m', default=10, type=int)
    parser.add_argument('--writetype', '-wt', default='deg', type=str)
    args = parser.parse_args()

    ser = None
    if args.serial:
        ser = serial.Serial('/dev/ttyACM0', 9600)

    _logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    _logger.setLevel(logging.INFO)
    handler.setLevel(logging.INFO)
    if args.debug:
        _logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
    _logger.addHandler(handler)

    fp = FacePos(ser, _logger, memory=args.memory, weight_str=args.weights)

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 3)

        for x, y, w, h in faces:
            px, py = (x + (w / 2.0), y + (h / 2.0))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.circle(frame, (int(px), int(py)), 2, (0, 255, 0), -1)
            fp.update(px, py)
        fp.write()
        cv2.imshow('frame', frame)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
