#!/usr/bin/env python
#-*- coding:utf-8 -*-
# =================  some key module need import  ==============
import numpy as np
import cv2
import mlpy
import pylab as pl
import neurolab as nl
# import sqlite3
import MySQLdb
import time

print u'Processing...'

# =================global varibal and initialize================
w_fg = 10
h_fg = 5
picflag = 3

file_name = 'results/results.txt'

# =================database initialize==========================



conn = MySQLdb.connect(host='192.168.42.1',user='root',passwd='heng130509',db='test',port=3306)
cur = conn.cursor()

def create_table():
    cur.execute("CREATE TABLE IF NOT EXISTS result(id REAL, name TEXT, value REAL)")

def data_entry(name, value):
    cur.execute("INSERT INTO result(id,name,value) VALUES(1,%s,%s)",(name,value))

    conn.commit()



# ==============Decision function================================
# Return classifier results
def getresult(simjg):
	'''some cda algorithm'''
	jg = []
	for j in xrange(0, len(simjg)):
		maxjg = -2
		nowii = 0
		for i in xrange(0,len(simjg[0])):
			if simjg[j][i]>maxjg:
				maxjg = simjg[j][i]
				nowii = i
		jg.append(len(simjg[0])-nowii)
	return jg


# ========Extract features from images with PCA algo.=============
# Return pic feature with PCA
def readpic(fn):
	'''read picture from train_data folder'''
	#return image feature code
	fnimg = cv2.imread(fn,cv2.IMREAD_COLOR)

	img =cv2.resize(fnimg, (700,350))
	w = img.shape[1]
	h = img.shape[0]

	w_interval = w / 20
	h_interval = h / 10

	alltz = []

	for now_h in xrange(0, h, h_interval):
		for now_w in xrange(0, w, w_interval):
			b = img[now_h:now_h + h_interval, now_w:now_w + w_interval, 0]
			g = img[now_h:now_h + h_interval, now_w:now_w + w_interval, 1]
			r = img[now_h:now_h + h_interval, now_w:now_w + w_interval, 2]

			btz = np.mean(b)
			gtz = np.mean(g)
			rtz = np.mean(r)

			alltz.append([btz, gtz, rtz])
	result_alltz = np.array(alltz).T
	pca = mlpy.PCA()
	pca.learn(result_alltz)
	result_alltz = pca.transform(result_alltz, k = len(result_alltz) / 2)
	result_alltz = result_alltz.reshape(len(result_alltz))
	return result_alltz

# ==================Training Process initialize=========================

train_x = []
d = []
sp_d = []
sp_d.append([0, 0, 1])
sp_d.append([0, 1, 0])
sp_d.append([1, 0, 0])
# read images data and extract images features

#=============From special text file read images info===================
# with open('file_name.txt', 'r') as f:
# 	for fn in f:
# 		print 'Reading %s...' %fn
# 		pictz = readpic(fn)
# 		train_x.append(pictz)
# 		d.append(sp_d[re.findall('^.*?([0-9])',fn)[0]-1])
# 	f.close()


# Retrive all training data set and extract img features with readpic function 

for ii in xrange(1, 4):
	# jj--picture id
	for jj in xrange(1, 20):
		fn = 'train_data' + '/' +str(ii) + '/' + 'p' + str(ii) + '-' + str(jj) + '.png'
		print 'Reading %s...' %fn

		pictz = readpic(fn)
		train_x.append(pictz)
		d.append(sp_d[ii-1])
myinput = np.array(train_x)
mytarget = np.array(d)
mymax = np.max(myinput)
netminmax = []
for i in xrange(0,len(myinput[0])):
	netminmax.append([0,mymax])

# ============Modeling with training error and neurolab lib=========================
print ''
print u'**************************************************'
print u'*********    neuron network completing   *********'
print u'*********                                *********'
print u'**************************************************'

print u'\n ...'
bpnet = nl.net.newff(netminmax,[80, 3])
print u'\ntraining...'
# =============================test components=========================================
# print mytarget
# print myinput


# ===================Attaion:Maybe model will be overfitting============================

err = bpnet.train(myinput, mytarget, epochs=1000,show=5,goal=1)

if err[len(err) - 1] > 0.4:
	print u'\n train false or something wrong....'
else:
	print u'\nfinished training...'

# ==================================Visulize model SSE===================================
# pl.plot(err)
# pl.xlabel('Epoch number')
# pl.ylabel('error ((default SSE)')



# =====================Testing start and valid-cross======================================
print u'testing start..............'
simd = bpnet.sim(myinput)
mysimd = getresult(simd)
print mysimd


print u'Simulation start...'
# ==================simulation start and REAL-Time detection with opencv===================

for ii in xrange(1,4):
	for jj in xrange(1,40):
		test_pic = 'test_data/'+ str(ii) + '/' +'ptest'+str(ii) + '-' + str(jj) +'.png'
		testpictz = np.array([readpic(test_pic)])
		simtest = bpnet.sim(testpictz)
		mysimtest = getresult(simtest)
		class_id = int(mysimtest[0])
		pic = 'ptest'+str(ii) + '-' + str(jj) +'.png'
		print pic
		print simtest
		print mysimtest
		# print mysimtest[0]
		# print type(mysimtest)
		#create_table()
		data_entry(pic,mysimtest[0])
		time.sleep(2)

cur.close()
conn.close()




