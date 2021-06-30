import serial
import struct
import time

state = 0
payload = list()

# +SPPDATA=1,028,
header = bytes([0x2B, 0x53, 0x50, 0x50, 0x44, 0x41, 0x54, 0x41, 0x3D, 0x31, 0x2C, 0x30, 0x32, 0x38, 0x2C])

class DataFrame():
    def __init__(self, buffer):
        self.device_addr = buffer[0]
        self.data = buffer[1:25]
        self.invariant = buffer[25:28]
        self.reserved = buffer[28:32]

    def __repr__(self):
        vals = struct.unpack("<6f", self.data)
        vals_str = "{:8.4f} {:8.4f} {:8.4f} {:8.4f} {:8.4f} {:8.4f}".format(vals[0], vals[1], vals[2], vals[3], vals[4], vals[5])
        invariant_str = "{:02X} {:02X} {:02X}".format(self.invariant[0], self.invariant[1], self.invariant[2])
        reserved_str = "{:02X} {:02X} {:02X} {:02X}".format(self.reserved[0], self.reserved[1], self.reserved[2], self.reserved[3])
        return "addr:{:02X}|data: {:s}| {:s} | {:s}".format(self.device_addr, vals_str, invariant_str, reserved_str)

def getframe(b):
    global state
    global payload

    b = int.from_bytes(b, byteorder='big')
    if state == -1 and b == 0x2B:
        state = 0
        return False
    elif state >= 0 and state < 14:
        if header[state + 1] == b:
            state = state + 1
        else:
            state = -1
        return False
    elif state >= 14 and state < 45:
        payload.append(b)
        state = state + 1
        return False
    elif state == 45:
        payload.append(b)
        state = -1
        return True


try:
    port_name = "/dev/tty.usbserial-A50285BI"
    port_bps = 921600
    serial_port = serial.Serial(port_name, port_bps, timeout=1)
    print(serial_port)
    serial_port.write("AT+SPPSEND=1,6,view=1\r\n".encode(encoding="ascii"))
    time.sleep(5)
    print("finish")
    serial_port.write("AT+SPPSEND=2,6,view=1\r\n".encode(encoding="ascii"))

    print("command sent")

    with open("data.hex", "wb") as f:

        for i in range(102400):
            data = serial_port.read()
            if getframe(data):
                frame = DataFrame(bytes(payload))
                print(frame)
                payload = []
            f.write(data)

    print("adsadsads")
    serial_port.close()

except Exception as e:
    print("error")
    print(e)





