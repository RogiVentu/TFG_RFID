import plotly.graph_objs as go
import plotly

import numpy as np
import random
import math


def getSemiCircleAreas(r,angle,x,y,scene):

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

	df = angle+60
	dt = angle-60

	print(angle,df,dt)

	for i in range(-r,r):
		for j in range(-r,r):
			h = float(math.sqrt(i**2 + j**2))
			if h < r:
				if h == 0:
					phi = angle
				else:
					aux = float(i)/float(h)
					phi = math.acos(aux)
					phi = math.degrees(phi)
				
				if phi < df and phi > dt:
					scene[x+j][y+i] += 1
					print(phi,i,j)
					print(x+j, y+i)
	return scene


scene = np.zeros((9,9))
sce = getSemiCircleAreas(4,90,4,4,scene)
print(sce)


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


"""
radius = 3
kernel = np.zeros((7, 7))

y,x = np.ogrid[-radius:radius+1, -radius:radius +1]

mask = x*x + y*y <= radius*radius


kernel[mask] = 1

#print mask 
#print kernel

aka = np.pad(kernel, ((0, 3), (0, 0)), 'constant', constant_values=(0,0))
"""