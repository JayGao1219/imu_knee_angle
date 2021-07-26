from PyImuSerial import *
from trans import *
import time

angle=input("请输入你想测试的角度\n")
angle=int(angle)
t=input("请输入收集数据时长(整数)\n")
t=int(t)
types=input("请输入关节的种类：1-书脊，2-盒子，3-肘关节，4-膝关节\n")
types=int(types)
is_new=input("请输入是否挪动imu的位置：1-挪动，0-没有挪动\n")
is_new=int(is_new)

## 到时候考虑用tk写个图形化界面吧，能稍微简化一下收集流程

f1=open('history.txt').read()
f1=f1.strip()
f2=open('history.txt','w')
f2.write(f1)

f1=f1.split('\n')
last=f1[-1].split('\t')
new_id=int(last[0])+1
is_new+=int(last[-1])

f2.write('\n%d\t%d\t%d\t%d\t%d'%(new_id,angle,t,types,is_new))
f2.close()

data_collection(t,new_id)
