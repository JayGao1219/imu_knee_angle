'''
代码作用
1. 做数据差值，使用linear方法，固定采样频率
2. 根据角度计算角速度
3. 生成角度计算的输入数据
'''

from scipy import interpolate

def get_data(path):
    with open(path) as f:
        data=eval(f.read())
    return data

def trans(path,diff=0.1):
    diff=0.1
    data=[]
    for item in path:
        data.append(get_data(item))
    begin=max(data[0][0][0],data[1][0][0])
    end=min(data[0][-1][0],data[1][-1][0])
   
    for i in range(len(data)):
        cur=get_inter(data[i],begin,end,diff)
        curpath=path[i].replace('data','newdata',1)
        store(cur,curpath)

if __name__=='__main__':
    path=['../data/imu1.txt','../data/imu2.txt']
    trans(path)
