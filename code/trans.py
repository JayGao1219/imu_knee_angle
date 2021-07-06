'''
代码作用
1. 做数据差值，使用linear方法，固定采样频率
2. 根据角度计算角速度
3. 生成角度计算的输入数据
'''

from scipy import interpolate
import math
import time

def get_data(path):
    with open(path) as f:
        data=eval(f.read())
    return data

def store(data,path):
    with open(path,'w') as f:
        f.write("%s\n"%str(time.time()))
        f.write("格式:[acc_x,acc_y,acc_z,pittch,yaw,row]\n")
        for item in data:
            f.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(item[1],item[2],item[3],item[4],item[5],item[6]))


def yaw_pitch_row(data):
    '''
    原始格式:[time,yaw,pittch,row,acc_x,acc_y,acc_z]
    转换格式:[time,acc_x,acc_y,acc_z,pittch,yaw,row]
    '''
    table={0:0,1:4,2:5,3:6,4:2,5:1,6:3}
    res=[]
    for i in range(len(data)):
        res.append(data[table[i]])
    return res

def get_inter(data,begin,end,diff):
    tot=begin+1
    whole=[]
    nx=[]
    while tot<end-1:
        whole.append([tot])
        nx.append(tot)
        tot+=diff
        pass
    x=[]
    for item in data:
        x.append(item[0])

    for i in range(len(data[0][1])):
        #对于每个数据点
        cur=[]
        for j in range(len(data)):
            cur.append(data[j][1][i])
        f=interpolate.interp1d(x,cur,kind='linear')
        y=f(nx)
        for j in range(len(whole)):
            whole[j].append(y[j])

    #计算角速度,前三个数据点是角速度
    for i in range(len(whole)-1):
        for j in range(1,4):
            whole[i][j]=(whole[i+1][j]-whole[i][j])/diff
    del whole[-1]

    #根据串口数据调试，让yaw,pittch,roll与x,y,z轴对应
    res=[]
    for item in whole:
        res.append(yaw_pitch_row(item))

    return res


def trans(path,diff=0.1):
    data=[]
    for item in path:
        data.append(get_data(item))
    begin=max(data[0][0][0],data[1][0][0])
    begin=math.floor(begin)
    end=min(data[0][-1][0],data[1][-1][0])
    end=math.ceil(end)
   
    for i in range(len(data)):
        cur=get_inter(data[i],begin,end,diff)
        curpath=path[i].replace('data','newdata',1)
        store(cur,curpath)

if __name__=='__main__':
    path=['../data/imu1.txt','../data/imu2.txt']
    trans(path)
