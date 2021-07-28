import numpy as np
from scipy import interpolate
import datetime
import math

from config import AngelConfing

def get_time(timestr):
	timestr=timestr.strip()
	cur=datetime.datetime.strptime(timestr,'%Y-%m-%d %H:%M:%S.%f')
	return cur.timestamp()

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
			cur.append(get_time(item[3]))
			for i in range(4,7):
				cur.append(float(item[i]))
			for i in range(7,10):
				cur.append(float(item[i]))

			data[cur_device].append(cur)
	#计算[g1',g2',g3'],需要先做差值，再计算

	return data

def get_inter(data,begin,end,diff):
	tot=begin
	whole=[]
	nx=[]
	while tot<end:
		whole.append([tot])
		nx.append(tot)
		tot=float('%.6f'%(tot+diff))

	x=[]
	for item in data:
		x.append(item[0])

	for i in range(1,len(data[0])):
		cur=[]
		for j in range(len(data)):
			cur.append(data[j][i])
		f=interpolate.interp1d(x,cur,kind='linear')
		y=f(nx)
		for j in range(len(whole)):
			#whole[j].append(y[j])
			whole[j].append(float(y[j]))

	return whole

def get_angular_acceleration(data,diff,index):
	vel_dot=[]
	for i in range(len(data)):
		cur=[]
		for j in range(len(index)):
			res=0.0
			if i >1 and i<len(data)-2:
				res=(data[i-2][index[j]]-8*data[i-1][index[j]]+8*data[i+1][index[j]]-data[i+2][index[j]])/(12*diff)
			elif i==1 or i==len(data)-2:
				res=(data[i+1][index[j]]-data[i-1][index[j]])/(2*diff)
			elif i==0:
				res=(data[i+1][index[j]]-data[i][index[j]])/diff
			else:
				res=(data[i][index[j]]-data[i-1][index[j]])/diff
			res=float('%.6f'%(res))
			cur.append(res)
		vel_dot.append(cur)
	for i in range(len(data)):
		data[i]+=vel_dot[i]

	return data

def c(tt):
	return math.cos(tt)

def s(tt):
	return math.sin(tt)

def sqrt(tt):
	return math.sqrt(tt)

def pow(tt):
	return math.pow(tt,2)

def get_pos(input_data,params,output):
	o1x=params[0][0]
	o1y=params[1][0]
	o1z=params[2][0]
	o2x=params[3][0]
	o2y=params[4][0]
	o2z=params[5][0]

	m=input_data.shape[0]
	for i in range(m):
		acc_joint1_x = input_data[i][4] * ( input_data[i][3] * o1y - input_data[i][4] * o1x ) - input_data[i][5] * ( input_data[i][5] * o1x - input_data[i][3] * o1z ) + ( input_data[i][7] * o1z - input_data[i][8] * o1y )
		acc_joint1_y = input_data[i][5] * ( input_data[i][4] * o1z - input_data[i][5] * o1y ) - input_data[i][3] * ( input_data[i][3] * o1y - input_data[i][4] * o1x ) + ( input_data[i][8] * o1x - input_data[i][6] * o1z )
		acc_joint1_z = input_data[i][3] * ( input_data[i][5] * o1x - input_data[i][3] * o1z ) - input_data[i][4] * ( input_data[i][4] * o1z - input_data[i][5] * o1y ) + ( input_data[i][6] * o1y - input_data[i][7] * o1x )

		acc_joint2_x = input_data[i][13] * ( input_data[i][12] * o2y - input_data[i][13] * o2x ) - input_data[i][14] * ( input_data[i][14] * o2x - input_data[i][12] * o2z ) + ( input_data[i][16] * o2z - input_data[i][17] * o2y )
		acc_joint2_y = input_data[i][14] * ( input_data[i][13] * o2z - input_data[i][14] * o2y ) - input_data[i][12] * ( input_data[i][12] * o2y - input_data[i][13] * o2x ) + ( input_data[i][17] * o2x - input_data[i][15] * o2z )
		acc_joint2_z = input_data[i][12] * ( input_data[i][14] * o2x - input_data[i][12] * o2z ) - input_data[i][13] * ( input_data[i][13] * o2z - input_data[i][14] * o2y ) + ( input_data[i][15] * o2y - input_data[i][16] * o2x )

		output[i][0] =  sqrt(\
			pow( input_data[i][0] - acc_joint1_x ) + pow( input_data[i][1] - acc_joint1_y ) + pow( input_data[i][2] - acc_joint1_z )) - \
		sqrt(\
			pow( input_data[i][9] - acc_joint2_x ) + pow( input_data[i][10] - acc_joint2_y) + pow( input_data[i][11] - acc_joint2_z ))

	return output


def get_axis(input_data,params,output):
	theta_1=params[0][0]
	theta_2=params[1][0]
	phi_1=params[2][0]
	phi_2=params[3][0]

	m=input_data.shape[0]
	for i in range(m):
		output[i][0]=sqrt(\
			pow(input_data[i][1]*s(theta_1)- input_data[i][2]*c(phi_1)*s(theta_1) )+\
			pow(input_data[i][2]*c(phi_1)*c(theta_1)- input_data[i][0]*s(phi_1) )+\
			pow(input_data[i][0]*c(phi_1)*s(theta_1)- input_data[i][1]*c(phi_1)*c(theta_1) ))-\
		sqrt(\
			pow(input_data[i][4]*s(theta_2)- input_data[i][5]*c(phi_2)*s(theta_2) )+\
			pow(input_data[i][5]*c(phi_2)*c(theta_2)- input_data[i][3]*s(phi_2) )+\
			pow(input_data[i][3]*c(phi_2)*s(theta_2)- input_data[i][4]*c(phi_2)*c(theta_2) ))

	return output

def get_angel_acc(j1,j2,a1,a2,g1,g2,g_dot1,g_dot2,o1,o2):
	c=np.zeros((3,1))
	x1=np.zeros((3,1))
	x2=np.zeros((3,1))
	y1=np.zeros((3,1))
	y2=np.zeros((3,1))

	acc1=np.zeros((2,1))
	acc2=np.zeros((2,1))

	a1_dot=np.zeros((1,3))
	a2_dot=np.zeros((1,3))

	p1=0.0
	p2=0.0
	q1=0.0
	q2=0.0
	angle_acc=0.0

	c=np.array([[1.0],[2.0],[3.0]])

	p1=np.cross(g1,o1.transpose())
	p2=np.cross(g1,p1)
	p3=np.cross(g_dot1,o1.transpose())
	a1_dot=a1-(p2+p3)

	p_1=np.cross(g2,o2.transpose())
	p_2=np.cross(g2,p_1)
	p_3=np.cross(g_dot2,o2.transpose())
	a2_dot=a2-(p_2+p_3)

	x1=np.cross(j1.transpose(),c.transpose())
	y1=np.cross(j1.transpose(),x1)
	x2=np.cross(j2.transpose(),c.transpose())
	y2=np.cross(j2.transpose(),x2)

	p1=np.dot(a1_dot,x1.transpose())[0][0]
	p2=np.dot(a1_dot,y1.transpose())[0][0]
	q1=np.dot(a2_dot,x2.transpose())[0][0]
	q2=np.dot(a2_dot,y2.transpose())[0][0]

	acc1=np.array([[p1],[p2]])
	acc2=np.array([[q1],[q2]])

	angle_acc=math.acos(np.dot(acc1.transpose(),acc2)[0][0]\
		/(np.linalg.norm(acc1)*np.linalg.norm(acc2)))
	return math.degrees(angle_acc)

class joint_angel():
	def __init__(self,data,test_data):
		self.DATASET_NUM=len(data[0])
		self.DELTA_T=AngelConfing.diff
		self.ITER_STEP=AngelConfing.ITER_STEP
		self.ITER_CNT=AngelConfing.ITER_CNT
		self.params_axis=np.zeros((4,1))
		self.params_pos=np.zeros((6,1))
		self.vj1=np.zeros((3,1))
		self.vj2=np.zeros((3,1))
		self.o1=np.zeros((3,1))
		self.o2=np.zeros((3,1))
		self.sname=''
		self.imu_data_1=np.array(data[0])
		self.imu_data_2=np.array(data[1])

		self.imu_test_data_1=np.array(test_data[0])
		self.imu_test_data_2=np.array(test_data[1])
		self.TEST_DATASET_NUM=len(test_data[0])

	def get_jacobian(self,func,input_data,params,output):
		m=input_data.shape[0]
		n=params.shape[0]

		out0=np.zeros((m,1))
		out1=np.zeros((m,1))
		param0=np.zeros((n,1))
		param1=np.zeros((n,1))

		for j in range(n):
			param0=params.copy()
			param1=params.copy()
			param0[j][0]-=self.ITER_STEP
			param1[j][0]+=self.ITER_STEP
			
			out1 = func(input_data,param1,out1)
			out0 = func(input_data,param0,out0)

			output[0:m,j:j+1]=(out1-out0)/(2*self.ITER_STEP)

		return output

	def gauss_newton(self,func,input_data,output,params):


		m=input_data.shape[0]
		n=params.shape[0]

		#jacobian
		jmat=np.zeros((m,n))
		r=np.zeros((m,1))
		tmp=np.zeros((m,1))

		pre_mse=0.0
		mse=0.0

		result=[]

		for i in range(self.ITER_CNT):			
			mse=0.0
			tmp=func(input_data,params,tmp)
			r=output-tmp
			jmat=self.get_jacobian(func,input_data,params,jmat)

			mse=np.dot(r.transpose(),r)
			mse/=m
			if abs(mse- pre_mse )<1e-6:
				print("均方根误差更新过小，已收敛")
				break

			pre_mse=mse
			a=np.dot(jmat.transpose(),jmat)

			b=np.linalg.pinv(a)
			c=np.dot(b,jmat.transpose())
			d=np.dot(c,r)
			result.append((mse,params.copy()))

			print("i=%d, mes:%lf"%(i,mse))

			params+=d

		pre=params
		minn=10000.0
		for item in result:
			if item[0]<minn:
				pre=item[1]
				minn=item[0]

		return pre

	def joint_pos(self):
		input_data=np.zeros((self.DATASET_NUM,18))
		output=np.zeros((self.DATASET_NUM,1))

		for i in range(self.DATASET_NUM):
			k=0
			for j in range(9):
				input_data[i][k]=self.imu_data_1[i][j]
				k+=1
			for j in range(9):
				input_data[i][k]=self.imu_data_2[i][j]
				k+=1
			output[i][0]=0.0

		for i in range(6):
			self.params_pos[i][0]=0.1

		self.params_pos=self.gauss_newton(get_pos,input_data,output,self.params_pos)

		self.o1=np.array([[self.params_pos[0][0]],[self.params_pos[1][0]],[self.params_pos[2][0]]])
		self.o2=np.array([[self.params_pos[3][0]],[self.params_pos[4][0]],[self.params_pos[5][0]]])

		print(self.o1,self.o2)

	def joint_axis(self):
		#计算关节轴向数据输入接口
		input_data=np.zeros((self.DATASET_NUM,6))
		output=np.zeros((self.DATASET_NUM,1))

		for i in range(self.DATASET_NUM):
			k=0
			for j in range(3,6):
				input_data[i][k]=self.imu_data_1[i][j]
				k+=1
			for j in range(3,6):
				input_data[i][k]=self.imu_data_2[i][j]
				k+=1
			output[i][0]=0.0

		for i in range(4):
			self.params_axis[i][0]=0.5

		self.params_axis=self.gauss_newton(get_axis,input_data,output,self.params_axis)

		self.vj1=np.array([[c(self.params_axis[2][0])*c(self.params_axis[0][0])],\
			[c(self.params_axis[2][0]*s(self.params_axis[0][0]))],\
			[s(self.params_axis[2][0])]])
		self.vj2=np.array([[c(self.params_axis[3][0])*c(self.params_axis[1][0])],\
			[c(self.params_axis[3][0])*s(self.params_axis[1][0])],\
			[s(self.params_axis[3][0])]])
		##做一个符号匹配
		flag=False
		if self.vj1[0][0]*self.vj2[0][0]<1e-10:
			flag=True
		if flag:
			self.vj1=-self.vj1
		print('j1,j2:')
		print(self.vj1)
		print(self.vj2)

	def test_angel(self):
		angle_acc = 0.0
		angle_gyr = 0.0
		angle_acc_gyr = 0.0
		prev_angle_gyr=0.0
		prev_angle_acc_gyr=0.0

		SUM=0.0
		cnt=0
		LAMBDA=0.01

		whole=[]

		for i in range(self.TEST_DATASET_NUM):
			cnt+=1
			a1=np.array([[self.imu_test_data_1[i][0],self.imu_test_data_1[i][1],self.imu_test_data_1[i][2]]])
			a2=np.array([[self.imu_test_data_2[i][0],self.imu_test_data_2[i][1],self.imu_test_data_2[i][2]]])
			g1=np.array([[self.imu_test_data_1[i][3],self.imu_test_data_1[i][4],self.imu_test_data_1[i][5]]])
			g2=np.array([[self.imu_test_data_2[i][3],self.imu_test_data_2[i][4],self.imu_test_data_2[i][5]]])
			g_dot1=np.array([[self.imu_test_data_1[i][6],self.imu_test_data_1[i][7],self.imu_test_data_1[i][8]]])
			g_dot2=np.array([[self.imu_test_data_2[i][6],self.imu_test_data_2[i][7],self.imu_test_data_2[i][8]]])

			angle_acc=get_angel_acc(self.vj1,self.vj2,a1,a2,g1,g2,g_dot1,g_dot2,self.o1,self.o2)

			
			aaa=np.dot(g1,self.vj1)-np.dot(g2,self.vj2)
			SUM=SUM+aaa[0][0]

			if cnt>3:
				cur={}
				angle_gyr=SUM*self.DELTA_T
				angle_acc_gyr=LAMBDA*angle_acc+(1- LAMBDA )*(prev_angle_acc_gyr+angle_gyr-prev_angle_gyr )
				print("angle_acc_gyr:",angle_acc_gyr)
				print("angle_acc:",angle_acc)
				# print("angle_gyr",angle_gyr)
				cur["angle_acc_gyr"]=angle_acc_gyr
				cur['angle_acc']=angle_acc
				cur["angle_gyr"]=angle_gyr
				whole.append(cur)
			
				
			if cnt<=3:
				prev_angle_acc_gyr=angle_acc
				prev_angle_gyr=angle_gyr
			else:
				prev_angle_acc_gyr=angle_acc_gyr
				prev_angle_gyr=angle_gyr

		with open(self.sname,'w') as f:
			f.write(str(whole))

def get_data(path):
	whole=[]
	with open(path) as f:
		context=f.read()
		context=context.split('\n')
		for item in context:
			if len(item)==0:
				continue
			cur=[]
			item=item.split('\t')
			for i in item:
				cur.append(float(i))
			whole.append(cur)
	return whole

def main(train,test):

	p1='../data/%d_1.txt'%(train)
	p2='../data/%d_2.txt'%(train)
	p3='../data/%d_1.txt'%(test)
	p4='../data/%d_2.txt'%(test)

	d1=get_data(p1)
	d2=get_data(p2)
	lens1=min(len(d1),len(d2))

	d1=d1[:lens1]
	d2=d2[:lens1]
	train_data=[d1,d2]

	d3=get_data(p3)
	d4=get_data(p4)
	lens2=min(len(d3),len(d4))

	d3=d3[:lens2]
	d4=d4[:lens2]
	test_data=[d3,d4]

	#去掉时间戳
	for i in range(len(train_data)):
		for j in range(len(train_data[i])):
			train_data[i][j]=train_data[i][j][1:]

	for i in range(len(test_data)):
		for j in range(len(test_data[i])):
			test_data[i][j]=test_data[i][j][1:]

	for i in range(len(train_data)):
		train_data[i]=get_angular_acceleration(train_data[i],AngelConfing.diff,[3,4,5])

	for i in range(len(test_data)):
		test_data[i]=get_angular_acceleration(test_data[i],AngelConfing.diff,[3,4,5])


	a=joint_angel(train_data,test_data)
	a.joint_axis()
	a.joint_pos()

	t1=np.dot(a.o1.transpose(),a.vj1)[0][0]
	t2=np.dot(a.o2.transpose(),a.vj2)[0][0]
	tt=(t1+t2)/2
	a.o1-=a.vj1*tt
	a.o2-=a.vj2*tt
	a.sname='../result/%d_%d.txt'%(train,test)
	a.test_angel()

if __name__ == '__main__':
	main(57,56)
