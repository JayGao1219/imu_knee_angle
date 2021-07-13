import numpy as np
from scipy import interpolate
import datetime

from config import AngelConfing


def get_raw_data(path='../data/1.csv'):
	data=[]
	#[a1,a2,a3,g1,g2,g3]
	with open(path) as f:
		context=f.read().split('\n')
		whole=[]
		for item in context:
			cur=item.split('\t')
			whole.append(cur)
		names=whole[0]
		whole=whole[1:]
		device_name=[]
		for item in whole:
			if item[0] not in device_name and len(item[0]):
				device_name.append(item[0])
		
		for i in range(len(device_name)):
			data.append([])

		for item in whole:
			if len(item)==0 or len(item[0])==0:
				continue
			cur_device=device_name.index(item[0])
			cur=[]
			cur.append(item[3])
			for i in range(4,7):
				cur.append(float(item[i]))
			for i in range(7,10):
				cur.append(float(item[i]))

			data[cur_device].append(cur)
	#计算[g1',g2',g3'],需要先做差值，再计算

	return data

def get_inter(data,begin,end,diff):
	pass


if __name__=='__main__':
	data=get_raw_data()
	# for item in data:
	# 	item[0]
	# data=get_inter(data,begin,end,AngelConfing.diff)
	print(data[0][0])
	print(len(data[0]),len(data[1]),len(data[2]))
	print(AngelConfing.diff)
	'''
	imu_joint_axis_data_fit()
	imu_joint_pos_data_fit()
	'''
