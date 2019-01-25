import json
import codecs
from pprint import pprint

from pyquaternion import Quaternion

from plotly.offline import iplot, init_notebook_mode
import plotly.graph_objs as go
import plotly.io as pio
import plotly
import plotly.plotly as py

import os
import numpy as np
import random

from tkinter import *



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



radius = 3
kernel = np.zeros((5, 5))

y,x = np.ogrid[-radius:radius+1, -radius:radius+1]
print(-radius)
print()
mask = x*x + y*y <= radius*radius


print mask 