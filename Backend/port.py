import serial

try:
    ser = serial.Serial('COM4', 9600)
except serial.SerialException:
    print("Arduino not connected — running without hardware")
    ser = None
