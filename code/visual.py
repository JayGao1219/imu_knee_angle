import numpy as np
from numpy.random import randn
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import stats
from pandas.core.frame import DataFrame

import os

from JointAngel import *
from config import AngelConfing

def get_result(train,test,flag=False):
	#flag: 是否重新运行代码
    root='../result/'
    f1='%d_%d.txt'%(train,test)
    files=os.listdir(root)

    if flag or f1 not in files:
    	main(train,test)
    with open(root+f1) as f:
        context=f.read()
        context=eval(context)
    return context[:1000]

def show_one(train,test,types=['angle_acc','angle_gyr']):
    res=get_result(train,test,True)
    data=[]
    colors=['green','red','blue']
    x=list(range(len(res)))
    for i in range(len(types)):
        data.append([])
    for i in range(len(res)):
        for j in range(len(types)):
            data[j].append(res[i][types[j]])
    plt.figure(19)
    for i in range(len(types)):
        plt.subplot(len(types),1,i+1)
        plt.plot(x,data[i],color=colors[i],label=types[i])
        plt.legend()
        plt.xlabel('0.01s')
        plt.ylabel('angle')
 
    plt.savefig('../image/%d-%d-16-%d.jpg'%(train,test,AngelConfing.window_size))
    plt.close()

if __name__ == '__main__':
    history=open('../data/history.txt').read().split('\n')
    history=history[1:]
    whole=[]
    for item in history:
        item=item.split('\t')
        cur=int(item[0])
        whole.append(cur)
    # for item in whole:
        # show_one(item,item)
    show_one(1,1)
