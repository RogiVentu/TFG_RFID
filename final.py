from pyquaternion import Quaternion
from utils import *
import numpy as np
import json
import csv
import math
import os
import random

#Read JSON DATA
def readJSON(jsonf, every):
	data = []
	with open(jsonf,'r') as f:
		x = 0
		for line in f:
			if x%every == 0:
				data.append(json.loads(line))
			x = x+1

	return data

#Take just the relevant data that we need
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

#Info antennas
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


def getAreas(data, size, scene):
	#Quaternion(w, x, y, z)
	for d in data:
		#robot 
		r_pos = d["robot_pose"][0]
		r_rot = d["robot_pose"][1]
		r_x = int(r_pos[1]*10 + 80)
		r_y = int(r_pos[0]*10 + 80)
		#print("x_before: " + str(r_pos[0]) + " / x_after: " + str(r_x) + "\n")
		#print("y_before: " + str(r_pos[1]) + " / y_after: " + str(r_y) + "\n")

		
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
		r = 15
		if d['rssi'] < -40:
			r = 5
		elif -40 < d['rssi'] < -60:
			r = 10
		else:
			r = 15
		
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

			""" % (j+1, i+1, scene[i,j], j-79, i-79)

	return posMax


def compareSceneWithTags(sceneTags, scene):
	max_sum = 0
	max_tag = 0
	worth_tag = sceneTags[0]
	count = 0
	for tag in sceneTags:
		count += 1
		multMatrixs = tag * scene
		#print(printScene(multMatrixs, 50))
		sumMat = multMatrixs.sum()
		if sumMat > max_sum:
			max_tag = count
			max_sum = sumMat
			worth_tag = tag
			#print(printScene(multMatrixs, 50))

	return (worth_tag, max_tag, max_sum)

def getReferenceTagsFromCSV(csvfile):
	refTags = []
	with open(csvfile, mode="r") as csv_file:
		for line in csv_file:
			#print(line)
			refTags.append(line)

	return refTags


print("Reading data...")
jsonData = readJSON('dades/location/S0_20DB.json', 1)
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

#3.- prova real
#epc -> 30347aae40004f55c682d54b (11 matches)
#epc -> bcea02adcf00002e9255cc80 (12 matches)
#epc -> 3034900b000000c000000003 (15 matches)
#epc -> 63 - 30349bc6e40363a4818626e6 (42 matches) ----- ( -4.46  ,   4.63 )
epc = "30347aae40004f55c682d54b"

#Data just for one EPC
print("\n\n----------------------- EPC CAPTION INFO -----------------------\n")
oneEpcData = getOneEpcData(relevantData, epc)
print("This EPC (" + epc + ") has " + str(len(oneEpcData)) + " captions\n")

#Creating scene...
size = 160 #-8 to 8 = 16x16 (json D) *10
scene = np.zeros((size,size))
scene = getAreas(oneEpcData, size, scene)
print("Scene " +str(size)+ "x" +str(size)+ " created")
#print(printScene(scene,size))

#Getting aproximated product position...
print(getMaxPos(scene))
#matPlot1fig(scene)
#matPlot(scene)


epcs_rt = [('bcc566dbb200002e923c1274', -1.67, 0.83 ), ('bc98abf11e00002e923b4f16', -2.32, -0.65)]

# Read csv reference tags
epcs_TEST = getReferenceTagsFromCSV("dades/reference_tags_pos.csv")
print(epcs_TEST)

scenes_rt = []
for ep in epcs_rt:
	scene_aux = np.zeros((size,size))
	data_rt = getOneEpcData(relevantData, ep[0])
	s_rt = getAreas(data_rt, size, scene_aux)
	scenes_rt.append(s_rt)
	#matPlot(s_rt)

# Looking for the nearest Tag to the scene...
print("\n\n----------------------- NEAREST REFERENCE TAG -----------------------\n")
nearestRT = compareSceneWithTags(scenes_rt, scene)
print("The tag number " + str(nearestRT[1]) + "with epc " + str(nearestRT[0])+ " is the nearest.\n")
print(getMaxPos(nearestRT[0]))

matPlot2fig(scene,nearestRT[0])
