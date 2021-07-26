f1=open('history.txt')
f1=f1.read().split('\n')
res=[]
for i in range(1,len(f1)):
	cur=f1[i].split('\t')
	cur[-1]=int(cur[-1])
	if i>1:
		if cur[-1]==1:
			cur[-1]=res[i-2][-1]+1
		else:
			cur[-1]=res[i-2][-1]
	res.append(cur)
f2=open('t.txt','w')
f2.write(f1[0])
for item in res:
	f2.write('\n%s\t%s\t%s\t%s\t%d'%(item[0],item[1],item[2],item[3],item[4]))
f2.close()
