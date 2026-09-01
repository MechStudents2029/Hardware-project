import serial

class SerialConnection:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1)

    def send(self, channel, angle):
        self.ser.write(f"{channel}:{angle}\n".encode())

    def close(self):
        self.ser.close()

