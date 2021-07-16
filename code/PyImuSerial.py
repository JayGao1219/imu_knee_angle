import serial
import struct
import time

##两个imu分开写
state1 = 0
payload1 = list()

state2 = 0
payload2 = list()

# +SPPDATA=1,028,
header1 = bytes([0x2B, 0x53, 0x50, 0x50, 0x44, 0x41, 0x54, 0x41, 0x3D, 0x31, 0x2C, 0x30, 0x32, 0x38, 0x2C])
# +SPPDATA=2,028,
header2= bytes([0x2B, 0x53, 0x50, 0x50, 0x44, 0x41, 0x54, 0x41, 0x3D, 0x32, 0x2C, 0x30, 0x32, 0x38, 0x2C])

class DataFrame():
    def __init__(self, buffer):
        self.device_addr = buffer[0]
        self.data = buffer[1:25]
        self.invariant = buffer[25:28]
        self.reserved = buffer[28:32]

    def __repr__(self):
        vals = struct.unpack("<6f", self.data)
        vals_str = "{:8.4f},{:8.4f},{:8.4f},{:8.4f},{:8.4f},{:8.4f}".format(vals[0], vals[1], vals[2], vals[3], vals[4], vals[5])
        return vals_str

def getframe1(b):
    global state1
    global payload1

    b = int.from_bytes(b, byteorder='big')
    if state1 == -1 and b == 0x2B:
        state1 = 0
        return False
    elif state1 >= 0 and state1 < 14:
        if header1[state1 + 1] == b:
            state1 = state1 + 1
        else:
            state1 = -1
        return False
    elif state1 >= 14 and state1 < 45:
        payload1.append(b)
        state1 = state1 + 1
        return False
    elif state1 == 45:
        payload1.append(b)
        state1 = -1
        return True

def getframe2(b):
    global state2
    global payload2

    b = int.from_bytes(b, byteorder='big')
    if state2 == -1 and b == 0x2B:
        state2 = 0
        return False
    elif state2 >= 0 and state2 < 14:
        if header2[state2 + 1] == b:
            state2 = state2 + 1
        else:
            state2 = -1
        return False
    elif state2 >= 14 and state2 < 45:
        payload2.append(b)
        state2 = state2 + 1
        return False
    elif state2 == 45:
        payload2.append(b)
        state2 = -1
        return True

def getval(cur):
    whole=[]
    res=cur.split(',')
    for item in res:
        whole.append(eval(item))
    return whole

def store(data,path):
    with open(path,'w') as f:
        f.write("%s\n"%str(time.time()))
        f.write("格式:[acc_x,acc_y,acc_z,g_x,g_y,g_z]\n")
        for item in data:
            f.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(item[0],item[1],item[2],item[3],item[4],item[5]))


def data_collection(second=30,name='imu'):
    global state1
    global payload1
    global state2
    global payload2
    port_name = "/dev/tty.usbserial-A50285BI"
    port_bps = 921600
    serial_port = serial.Serial(port_name, port_bps, timeout=1)
    print(serial_port)
    serial_port.write("AT+SPPSEND=1,6,view=1\r\n".encode(encoding="ascii"))
    time.sleep(3)
    serial_port.write("AT+SPPSEND=2,6,view=1\r\n".encode(encoding="ascii"))

    print("开始收集数据")
    begin=time.time()

    path1='../data/%s1.txt'%name
    path2='../data/%s2.txt'%name
    imu1=[]
    imu2=[]

    while True:
        data=serial_port.read()
        cur=time.time()
        if cur-begin>second:
            print("数据收集完毕")
            break
        if getframe1(data):
            frame = DataFrame(bytes(payload1))
            frame = getval(str(frame))
            imu1.append(frame)
            payload1 = []
        if getframe2(data):
            frame = DataFrame(bytes(payload2))
            frame = getval(str(frame))
            imu2.append(frame)
            payload2 = []

    lens=min(len(imu1),len(imu2))
    imu1=imu1[:lens]
    imu2=imu2[:lens]

    store(imu1,path1)
    store(imu2,path2)


if __name__=='__main__':
    data_collection(10,name='90_1')
