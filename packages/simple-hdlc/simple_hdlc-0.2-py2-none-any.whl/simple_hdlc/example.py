from simple_hdlc import HDLC
import serial
import time
import logging

logging.basicConfig(level=logging.WARNING)

s = serial.serial_for_url('/dev/ttyUSB0', baudrate=115200)
h = HDLC(s)

def frame_callback(data):
    print(data.encode("hex"))

h.startReader(frame_callback)

while 1:
    time.sleep(3.0)
    h.sendFrame(b"\x00\x00\x01\xff\xff\xff\xff")
    h.sendFrame(b"\x00\x00\x00")
    time.sleep(3.0)
    h.sendFrame(b"\x00\x00\x01\xff\x00\xff\xff")
    h.sendFrame(b"\x00\x00\x00")