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

def createScene(size):
	scene = []
	for i in xrange(size):
		scene.append([])
	for i in xrange(size):
		for j in xrange(size):
			scene[i].append(j)
			scene[i][j] = 0
	return scene

def readJSON(jsonf):
	data = []
	with open(jsonf,'r') as f:
		for line in f:
			data.append(json.loads(line))

	return data

def getRelevantVariables(data):
#at the moment: epc,robot_pose,RSSI,ts,ANTENNA_PORT,device_id
#return a list of dictionaries
	relData = []
	for d in data:
		relData.append({'epc':d['epc'],
			'robot_pose':d['robot_pose'],
			'rssi':d['RSSI'],
			'ts':d['ts'],
			'antenna_port':''.join(d['ANTENNA_PORT']),
			'device_id':d['device_id']})

	return relData

def getAntennas(data):

	antList = {"reader-01/4":"L1",
		"reader-01/3":"L2",
		"reader-01/2":"L3",
		"reader-01/1":"L4",
		"reader-02/1":"R1",
		"reader-02/2":"R2",
		"reader-02/3":"R3",
		"reader-02/4":"R4"}

	for d in data:
		try:
			d["antenna_id"] = antList[d["device_id"] + "/" + d["antenna_port"]]
		except:
			d["antenna_id"] = "L3"
	return data

def getTransRotAntennas(data):
	#make a list[trans,rot] where trans and rot are lists too
	for d in data:
		if d["antenna_id"] == "L1":
			d["ant_pose"] = [[0.15,0.17,0.03],[0.5,-0.5,-0.5,-0.5]]
		elif d["antenna_id"] == "L2":
			d["ant_pose"] = [[0.15,0.63,0.03],[0.5,-0.5,-0.5,-0.5]]
		elif d["antenna_id"] == "L3":
			d["ant_pose"] = [[0.15,1.1,0.03],[0.5,-0.5,-0.5,-0.5]]
		elif d["antenna_id"] == "L4":
			d["ant_pose"] = [[0.15,1.56,0.03],[0.5,-0.5,-0.5,-0.5]]
		elif d["antenna_id"] == "R1":
			d["ant_pose"] = [[0.15,0.17,0.14],[0.5,0.5,0.5,-0.5]]
		elif d["antenna_id"] == "R2":
			d["ant_pose"] = [[0.15,0.63,0.14],[0.5,0.5,0.5,-0.5]]
		elif d["antenna_id"] == "R3":
			d["ant_pose"] = [[0.15,1.1,0.14],[0.5,0.5,0.5,-0.5]]
		elif d["antenna_id"] == "R4":
			d["ant_pose"] = [[0.15,1.56,0.14],[0.5,0.5,0.5,-0.5]]


	return data


def getAreas(data,scene):
	#Quaternion(w, x, y, z)

	for d in data:
		#robot 
		r_pos = d["robot_pose"][0]
		r_rot = d["robot_pose"][1]
		r_x = r_pos[0]
		r_y = r_pos[1]
		r_degrees = Quaternion(r_rot[3],r_rot[0],r_rot[1],r_rot[2]).degrees
		#antenna
		a_pos = d["ant_pose"][0]
		a_rot = d["ant_pose"][1]
		#a_degrees = Quaternion(a_rot[3],a_rot[0],a_rot[1],a_rot[2]).degrees
		if "L" in d["antenna_id"]:
			a_degrees = 90
		elif "R" in d["antenna_id"]:
			a_degrees = -90

		scene[r_x][r_y] = 1
		print r_degrees + a_degrees


	return scene

def printScene(scene, size):
	#this method should be removed for a plot library
	finalOut = ""
	for i in range(0,size):
		for j in range(0,size):
			finalOut += str(scene[i][j]) + "|"
		finalOut += "\n"
		for l in range(0, size*2-1):
			finalOut += "-"
		finalOut += "\n"

	return finalOut

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





print("Creating scene...")
size = 25
scene = createScene(size)
print("Scene " +str(size)+ "x" +str(size)+ " created")

print("Reading data...")
jsonData = readJSON('dades/181005-080248-C2.json')
print("Done.")

print("Getting important variables...")
relevantData = getRelevantVariables(jsonData)
print("Done.")

print("Getting antennas which made the caption...")
relevantData = getAntennas(relevantData)
print("Done")

print("Getting antennas position and directions...")
relevantData = getTransRotAntennas(relevantData)
print("Done")

#print(relevantData)
"""
print("Getting aproximated areas...")
sceneArea = getAreas(relevantData,scene)
print("Done")
"""
#print(printScene(sceneArea,size))

#Plotly 
#2D
printPlotlyScene2D(relevantData)
#3D
#printPlotlyScene3D(relevantData)

#Canvas
#printByCanvas(relevantData)


#print(type(relevantData[0]["robot_pose"]))




#print "Write data... \nFormat: posX,posY,dir \nExample: 33,70,top"
#x,y,dire = raw_input().split(",")
#print "Detection saved in position ("+str(x)+","+str(y)+") looking at " + dire + "."
