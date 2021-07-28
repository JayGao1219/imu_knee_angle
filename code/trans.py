'''
代码作用
1. 做数据差值，使用linear方法，固定采样频率
2. 根据角度计算角速度
3. 生成角度计算的输入数据
'''

from scipy import interpolate
import math
import time
import numpy as np
import os

from config import AngelConfing

def MAD(dataset,n):
    median = np.median(dataset)
    deviations = abs(dataset - median)
    mad = np.median(deviations)
    remove_idx = np.where(abs(dataset - median) >  n * mad)
    cur=[]
    for item in list(remove_idx[0]):
        cur.append(dataset[item])
    print(cur)
    return list(remove_idx[0])

def three_sigma(dataset, n= 3):
    mean = np.mean(dataset)
    sigma = np.std(dataset)
    remove_idx = np.where(abs(dataset - mean) > n * sigma)
    cur=[]
    for item in list(remove_idx[0]):
        cur.append(dataset[item])
    print(cur)
    return list(remove_idx[0])

def get_data(path):
    with open(path) as f:
        data=eval(f.read())
    return data

def store(data,path,info):
    with open(path,'w') as f:
        f.write("%s\n"%str(time.time()))
        f.write("%s\n"%str(info))
        for item in data:
            f.write("%f\t%f\t%f\t%f\t%f\t%f\n"%\
                (item[1],item[2],item[3],item[4],item[5],item[6]))

def removeOutliers(remove_idx,data):
    res=[]
    for i in range(len(data)):
        if i not in remove_idx:
            res.append(data[i])
    return res

def get_inter(data,begin,end,diff):
    tot=begin
    whole=[] #差值后的数据
    nx=[] #新的 x
    while tot<end:
        whole.append([tot])
        nx.append(tot)
        tot+=diff

    x=[] #旧的 x
    for item in data:
        x.append(item[0])

    for i in range(len(data[0][1])):
        #对于每个数据点,做线性差值
        cur=[]
        for j in range(len(data)):
            cur.append(data[j][1][i])
        f=interpolate.interp1d(x,cur,kind='linear')
        y=f(nx)
        for j in range(len(whole)):
            whole[j].append(y[j])

    return whole

    #去掉离群点
    '''
    convert=list(map(list,zip(*res)))
    remove_idx=[]
    for i in range(4,6):
        print(i)
        
        #cur=MAD(convert[i],3)
        cur=three_sigma(convert[i],2)
        print(cur)
        print('\n')
        remove_idx+=cur

    res=removeOutliers(remove_idx,res)
    
    for i in range(len(res)):
        for j in range(4,7):
            if res[i][j]>100:
                res[i][j]=100
            if res[i][j]<-100:
                res[i][j]=-100
    '''
    
def trans(path='',diff=0.0):
    root_path='../data/'
    if diff==0.0: 
        # diff可以自己指定，如果没指定，就使用默认的
        diff=AngelConfing.diff
    if len(path)==0:
        # 如果不指定，默认将'../data' 下的所有文件转换到新的文件夹下
        all_path=[]
        dirs=os.listdir(root_path)
        if '.DS_Store' in dirs:
            dirs.remove('.DS_Store')
    else:
        all_path=[path]

    for item in all_path:
        cur_data=get_data(root_path+item)
        begin=math.ceil(data[0][0])
        end=math.floor(data[-1][0])
        cur_data=get_inter(cur_data,begin,end,diff)
        cur_path=item.replace('data','newdata',1)

        store(cur_data,cur_path,[begin,end,diff])
        # data.append(get_data(root_path + item))


    ##begin 和 end 不如放到 JointAngel去判断
    #### 记得去改一下，或者再写一个外包函数去做判断，在JointAngel的基础上
   

if __name__=='__main__':
    # path=['../data/gj1.txt','../data/gj2.txt']
    trans()
