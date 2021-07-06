'''
代码作用
1. 做数据差值，使用linear方法，固定采样频率
2. 根据角度计算角速度
3. 生成角度计算的输入数据
'''

from scipy import interpolate
import math

def get_data(path):
    with open(path) as f:
        data=eval(f.read())
    return data

def store(data,path):
    with open(path,'w') as f:
        f.write(str(data))

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
    return whole


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
