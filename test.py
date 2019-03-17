import json
import codecs
from pprint import pprint

from pyquaternion import Quaternion
from utils import getSemiCircleAreas
"""
from plotly.offline import iplot, init_notebook_mode
import plotly.graph_objs as go
import plotly.io as pio
import plotly
import plotly.plotly as py
"""
import os
import numpy as np
import random
import math

#from tkinter import *


def readJSON(jsonf, every):
	data = []
	with open(jsonf,'r') as f:
		x = 0
		for line in f:
			if x%every == 0:
				data.append(json.loads(line))
			x = x+1

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


def getOneEpcData(data, epc):

	epcData = []
	for d in data:
		if d['epc'] == epc:
			epcData.append(d)

	return epcData

def addFakeTags(scene):
	#12 fake tags
	for i in range(1,5):
		x = i*10
		for j in range(1,5):
			y = j*10
			scene[x][y] += 10
			for t in range(-9,9):
				k = t + x
				for h in range(-9,9):
					#hipotenusa
					l = h + y
					hipo = float(math.sqrt(t**2 + h**2))
					print(hipo, k, l)

					scene[k][l] = 10 - int(hipo)
	return scene

def getAreas(data, size, scene):
	#Quaternion(w, x, y, z)
	for d in data:
		#robot 
		r_pos = d["robot_pose"][0]
		r_rot = d["robot_pose"][1]
		r_x = int(r_pos[0]) + 25
		r_y = int(r_pos[1]) + 25

		
		r_degrees = Quaternion(r_rot[3],r_rot[0],r_rot[1],r_rot[2]).degrees
		#antenna
		if r_rot[2] < 0:
			r_degrees = r_degrees * (-1)
		a_pos = d["ant_pose"][0]
		a_rot = d["ant_pose"][1]
		#a_degrees = Quaternion(a_rot[3],a_rot[0],a_rot[1],a_rot[2]).degrees
		if "L" in d["antenna_id"]:
			a_degrees = 90
		elif "R" in d["antenna_id"]:
			a_degrees = -90
		
		deg = r_degrees + a_degrees
		
		#agafar la mida (radi) segons el rssi (quan mes gran, mes petit es el radi)
		r = 4
		if d['rssi'] < -40:
			r = 2
		elif -40 < d['rssi'] < -60:
			r = 3
		else:
			r = 4

		scene = getSemiCircleAreas(r,deg,r_x,r_y,scene)
	return scene

def printScene(scene, size):
	finalOut = ""
	for i in range(0,size):
		for j in range(0,size):
			finalOut += str(int(scene[i][j])) + "|"
		finalOut += "\n"
		for l in range(0, size*2-1):
			finalOut += "-"
		finalOut += "\n"

	return finalOut

def getMaxPos(scene):

	i,j = np.unravel_index(scene.argmax(), scene.shape)
	posMax = """Position in the scene: (%s, %s).
Value (number of captations): %s.
Real position: (%s, %s).

			""" % (j+1, i+1, scene[i,j], j-24, i-24)

	return posMax

#jsons
#1.-181005-080248-C2.json
#2.-181127-125006-D1.json
print("Reading data...")
jsonData = readJSON('dades/181005-080248-C2.json', 1)
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

#FOR ONLY ONE EPC 
#1.-json
#epc -> 08283097906a6bd50731e70d27040400 (2 matches)
#epc -> 082863f1e52a91e435af41257f010400 (3 matches)
#epc -> 08285fca0e7c1254463de57b7f208400 (7 matches)
#epc -> 08283289d4bb6a704e4cf7531b400400 (10 matches)
#epc -> 082812b8ea3cc443385d9e3f8b818400 (15 matches)
#epc -> 082811357df0b5c347178e328ba08400 (25 matches)
#epc -> 082811357f7754d72d4a0ce227818400 (32 matches)
#epc -> 08286e5a6486616646ad89e07f208400 (33 matches)
#epc -> 082823768fc931dc5623205540c00400 (36 matches)

#2.-json
#epc -> bcc8c8762300002e92480130 (23 matches, group 2_6)
#epc -> bc8c3448e600002e92479b8a (3 matches, group 1_1)
#epc -> bcbb656f2400002e92398a42 (15 matches, group 1_1)
#epc -> bce8efaa0e00002e923294b4 (13 matches, group 2_9)

epc = "082811357f7754d72d4a0ce227818400"

print("Data just for one EPC")
oneEpcData = getOneEpcData(relevantData, epc)
print("This EPC (" + epc + ") has " + str(len(oneEpcData)) + " captions")
print("Done")

print("Creating scene...")
size = 50
scene = np.zeros((size,size))
scene = addFakeTags(scene)
print(printScene(scene,size))
scene = getAreas(oneEpcData, size, scene)
print("Scene " +str(size)+ "x" +str(size)+ " created")

#print(printScene(scene,size))

print("Getting aproximated product position...\n")
print(getMaxPos(scene))

#Plotly 
#2D
#printPlotlyScene2D(relevantData)
#3D
#printPlotlyScene3D(relevantData)

#Canvas
#printByCanvas(relevantData)
