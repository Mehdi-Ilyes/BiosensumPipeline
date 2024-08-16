# verify_serial.py
import serial

try:
    ser = serial.Serial()
    print("pyserial imported and Serial class available.")
except AttributeError:
    print("Error: pyserial.Serial not found.")