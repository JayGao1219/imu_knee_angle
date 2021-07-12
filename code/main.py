from PyImuSerial import *
from trans import *

name=input("请输入受试者姓名")
t=input("请输入收集数据时长(整数)")
t=int(t)

diff=input("请输入时间间隔")
if len(diff):
	diff=float(diff)
else:
	diff=0.1

data_collection(t,name)

path1='../data/%s1.txt'%name
path2='../data/%s2.txt'%name
path=[path1,path2]

trans(path,diff)

f1=open('history.txt').read()
f2=open('history.txt','w')
f2.write(f1)
f2.write('\n')
f2.write('%s\t%d\t%f'%(name,t,diff))
f2.close()