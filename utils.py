from pyquaternion import Quaternion

import numpy as np
import random
import math

import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt

def getSemiCircleAreas(r,angle,x,y,scene):

	#print("x:" + str(x) + " - y:" + str(y))

	"""
	if angle > 180:
		angle = angle -180
	elif angle > 0 and angle < 180:
		angle = angle
	elif angle < 0 and angle > -180:
		angle = angle + 180
	else:
		angle = angle + 360
	"""
	if angle < 0:
		angle = angle + 360
	df = angle+60
	dt = angle-60

	#print(angle,df,dt)

	for i in range(-r,r):
		for j in range(-r,r):
			if x+j > 159 or x+i > 159:
				continue
			h = float(math.sqrt(i**2 + j**2))
			if h < r:
				if h == 0:
					phi = angle
				else:
					aux = float(i)/float(h)
					phi = math.acos(aux)
					phi = math.degrees(phi)
				if i <= 0 and j > 0:
					phi = 360 - phi
				elif i >= 0 and j > 0:
					phi = 360 - phi
				
				#print('dt:' + str(dt) + ' / phi:' + str(phi) + " / df:" + str(df))
				if dt < 0:
					if phi < df or phi > (dt+360):
						#print('x:' + str(x) + '/ y:' + str(y))
						#print('j:' + str(j) + '/ i:' + str(i))
						scene[x+j][y+i] += 1
						#print(phi,i,j)
						#print(x+j, y+i) 
				else:
					if phi < df and phi > dt:
						#print('x:' + str(x) + '/ y:' + str(y))
						#print('j:' + str(j) + '/ i:' + str(i))
						if(x+j < 160 and x+j >= 0 and y+i < 160 and y+i >= 0):
							scene[x+j][y+i] += 1
							#print(phi,i,j)
							#print('this is x,y --> ' + str(x) + ',' + str(y))
							#print(x+j, y+i)
	return scene


#scene = np.zeros((9,9))
#sce = getSemiCircleAreas(4,300,4,4,scene)
#print(sce)
#print(Quaternion(0.7446857431941718, 0.0, 0.0, -0.6674152709395734 ).degrees)


def addFakeTags(size):
	sceneTags = []
	for x in range(1,5):
		x = x*10
		for y in range(1,5):
			y = y*10
			scene = np.zeros((size,size))
			sceneTags.append(addFakeCaptions(scene,x,y))
	return sceneTags

def addFakeCaptions(scene, x,y):
	for i in range(-9,9):
		k = i + x
		for j in range(-9,9):
			#hipotenusa
			l = j + y
			hipo = float(math.sqrt(i**2 + j**2))
			if hipo <= 10:
				scene[k][l] = 10 - int(hipo)

	return scene

def printPlotlyScene2D(data):

	x = []
	y = []
	colors = []
	sz = []	
		
	for d in data:
		#de moment agafem la pos del robot
		try:
			if d["robot_pose"][0][0] in x:
				if d["robot_pose"][0][1] in y:
					continue
			x.append(d["robot_pose"][0][0])
			y.append(d["robot_pose"][0][1])

		except:
			continue

		colors.append(random.randint(0,39))
		sz.append(int(d["rssi"][0])*(-1))

	fig = go.Figure()
	fig.add_scatter(x=x,
				y=y,
                mode='markers',
                marker={'size': sz,
                        'color': colors,
                        'opacity': 0.4,
                        'colorscale': 'Viridis',
                        'line' : dict(
                        	color = 'rgb(0,0,0)',
                        	width = 0)                        
                       });
	plotly.offline.plot(fig,auto_open=True)


def printPlotlyScene3D(data):

	x = []
	y = []
	z = []
	colors = []
	sz = []
	
	for d in data:
		#de moment agafem la pos del robot

		try:
			if d["robot_pose"][0][0] in x:
				if d["robot_pose"][0][1] in y:
					continue
			x.append(d["robot_pose"][0][0])
			y.append(d["robot_pose"][0][1])
			
		except:
			continue

		z.append(0.024)
		colors.append(random.randint(1,100))
		sz.append(int(d["rssi"][0])*(-1))



	trace1 = go.Scatter3d(x=x,
				y=y,
				z=z,
                mode='markers',
                marker={'size': sz,
                        'color': colors,
                        'opacity': 0.6,
                        'colorscale': 'Viridis',
                        'line' : dict(
                        	color = 'rgb(0,0,0)',
                        	width = 0)
                       });

	dat = [trace1]
	layout = go.Layout(
    	margin=dict(
        	l=0,
        	r=0,
        	b=0,
        	t=0
    	)
	)

	fig = go.Figure(data=dat, layout=layout)
	plotly.offline.plot(fig,auto_open=True)

def printByCanvas(data):

	root = Tk()

	canvas = Canvas(root, width=400, height=400, bg='white')
	canvas.pack()

	for d in data:
		x = d["robot_pose"][0][0] + 200
		y = d["robot_pose"][0][1] + 200

		canvas.create_arc(x-20,y-40,x+20,y, start=0, extent=180)


	root.mainloop()


def initScene(size):
	scene = []
	for i in xrange(size):
		scene.append([])
	for i in xrange(size):
		for j in xrange(size):
			scene[i].append(j)
			scene[i][j] = 0
	return scene

def matPlot(scene):

	plt.close()	
	ax = sn.heatmap(scene, annot=False, fmt=".3f", cmap = 'Blues')
	plt.show()

def matPlot1fig(scene):

	f = plt.figure("Capted EPC")
	ax = sn.heatmap(scene, annot=False, fmt=".3f", cmap = 'Blues')
	ax.invert_yaxis()
	f.show()

	raw_input()

def matPlot2fig(scene, tagscene):

	f = plt.figure("Capted EPC")
	ax = sn.heatmap(scene, annot=False, fmt=".3f", cmap = 'Blues')
	ax.invert_yaxis()
	f.show()
	g = plt.figure("Most Equal Reference TAG")
	bx = sn.heatmap(tagscene, annot=False, fmt=".3f", cmap = 'Blues')
	bx.invert_yaxis()
	g.show()

	raw_input()