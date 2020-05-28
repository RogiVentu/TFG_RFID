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

	print(scene)
	i,j = np.unravel_index(scene.argmax(), scene.shape)
	posMax = """Position in the scene: (%s, %s).
Value (number of captations): %s.
Real position: (%s, %s).

			""" % (j+1, i+1, scene[i,j], j-79, i-79)

	return posMax


def compareSceneWithTagsMULT(sceneTags, scene):
	max_sum = 0
	max_tag = 0
	worth_tag = sceneTags[0]
	num_tag = sceneTags[1]
	epc_tag = sceneTags[2]
	count = 0

	topTags = []
	for tag in sceneTags:
		count += 1
		multMatrixs = tag[0] * scene
		#print(printScene(multMatrixs, 50))
		sumMat = multMatrixs.sum()
		if sumMat > max_sum:
			max_tag = count
			max_sum = sumMat
			worth_tag = tag[0]
			num_tag = tag[1]
			epc_tag = tag[2]
			#print(printScene(multMatrixs, 50))

		topTags.append([sumMat, tag[1]])	

	topTags.sort(reverse=True)
	minValue = topTags[len(topTags) - 1][0]
	maxValue = topTags[0][0]


	#print(minValue , maxValue)
	normalizedData = []
	for tag in topTags:
		tag[0] = (tag[0] - minValue)/(maxValue - minValue)
		normalizedData = append([tag[1], tag[0]])
		#print(str(tag[1]) + ': ' + str(tag[0]))

	return (worth_tag, max_tag, max_sum, num_tag, epc_tag, normalizedData)

def compareSceneWithTagsSUMREST(sceneTags, scene):

	max_sum = 0
	max_tag = 0
	worth_tag = sceneTags[0]
	num_tag = sceneTags[1]
	epc_tag = sceneTags[2]

	topTags = []
	for tag in sceneTags:
		suma = 0
		sceneTag = tag[0]
		for i in range(0, len(scene)):
			for j in range(0, len(scene)):
				if(sceneTag[i][j] > 0 and scene[i][j] > 0):
					suma += sceneTag[i][j] + scene[i][j]
				else:
					suma -= sceneTag[i][j] - scene[i][j]

		topTags.append([suma , tag[1]])
		#print('EPC NUM: ' + str(tag[1]) + ' - SUMA:' + str(suma))

		#Fer top de sumas, el que sigui mes alt se pto prende


	topTags.sort(reverse=True)
	minValue = topTags[len(topTags) - 1][0]
	maxValue = topTags[0][0]

	
	#print(minValue , maxValue)
	normalizedData = []

	for tag in topTags:
		tag[0] = (tag[0] - minValue)/(maxValue - minValue)
		normalizedData.append([tag[1], tag[0]])
		#print(str(tag[1]) + ': ' + str(tag[0]))

				
	#print(normalizedData)
	return (worth_tag, max_tag, max_sum, num_tag, epc_tag, normalizedData)

def getReferenceTagsFromCSV(csvfile):
	refTags = []
	with open(csvfile, mode="r") as csv_file:
		for line in csv_file:
			#print(line)
			oneRefTag = line.split(',', 3)
			oneRefTag[3] = oneRefTag[3].replace('\n', '');
			refTags.append(oneRefTag)

	return refTags

def triangulatePoints( pounders , epcs):

	a = pounders[1]
	b = pounders[2]
	c = pounders[3]

	atag = []
	btag = []
	ctag = []

	for epc in epcs:
		if a[0] == epc[0]:
			atag = epc
		if b[0] == epc[0]:
			btag = epc
		if c[0] == epc[0]:
			ctag = epc

	print(a , b , c)

	print(atag, btag, ctag)

	xn = a[1]*float(atag[2]) + b[1]*float(btag[2]) + c[1]*float(ctag[2])
	xd = a[1] + b[1] + c[1]

	x = xn / xd

	yn = a[1]*float(atag[3]) + b[1]*float(btag[3]) + c[1]*float(ctag[3])
	yd = a[1] + b[1] + c[1]

	y = yn / yd

	print('Triangulation pos -> ' + str(x) + " , " + str(y))

def nPoints( pounders , epcs , n):

	xn = 0
	xd = 0

	yn = 0
	yd = 0

	for i in range(0 , n):
		for epc in epcs:
			if(pounders[i][0] ==  epc[0]):
				xn += pounders[i][1] * float(epc[2])
				xd += pounders[i][1]

				yn += pounders[i][1] * float(epc[3])
				yd += pounders[i][1]

	x = xn / xd
	y = yn / yd

	print('N-Points pos -> ' + str(x) + " , " + str(y));


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
#68 -> 30349bc6fc11f5aab509b27d
#29 -> 30349f46f00561844d3cca97
#41 -> 303602c44408fc7be14d1a1b
#54 -> 30349bb868034fa0b833ebc4
#30 -> 303602c44408fc407fc0fc5f
#64 -> 30349bd2a40d13aa89f060fb
#65 -> 30349bc6e40363aab2672b65
#66 -> 30349bc7140359aa9c816b87
#27 -> 311602967c7a95ebef000000
#42 -> 30349bc718025faab25a4224
#69 -> 30349bc718025fa76dee56df
#34 -> 303600005c073348a0ddb948
#36 -> 303602c44408fc6fc78ec4e5
#37 -> 303400000061a83dd0a091b9
#39 -> 303602c44408fc7e13907e57 ( 65 matches )
#41 -> 303602c44408fc79a24988c4
#46 -> 30349bb6d408458b7b7b6acd ( 75 matches )
#51 -> 30349bb7f80935be9c3f927f
#43 -> 30349bb5b015e79f8a669ed7
epc = "30349bb5b015e79f8a669ed7"

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



#epcs_rt = [['bc94e35bb000002e922afb74', -2.17, 0.80 ], ['bcadf7973500002e9238fd56', -2.26, -0.10]]

# Read csv reference tags
epcs_RT_real = getReferenceTagsFromCSV("dades/reference_tags_pos.csv")
#print(epcs_TEST)
scenes_rt = []
for ep in epcs_RT_real:
	rt_data = []
	scene_aux = np.zeros((size,size))
	data_rt = getOneEpcData(relevantData, ep[1].lower())
	s_rt = getAreas(data_rt, size, scene_aux)
	rt_data = [s_rt, ep[0], ep[1]]
	scenes_rt.append(rt_data)
	#matPlot(s_rt)

#print(scenes_rt)






# Looking for the nearest Tag to the scene...
print("\n\n----------------------- NEAREST REFERENCE TAG -----------------------\n")
#nearestRT = compareSceneWithTagsMULT(scenes_rt, scene)
nearestRT = compareSceneWithTagsSUMREST(scenes_rt, scene)

#Centro de triangulo sin pesos -> https://es.wikihow.com/calcular-el-centro-de-gravedad-de-un-tri%C3%A1ngulo
#Fer el mateix pero multiplicant les coordenades x y y per el pes d'aquestes -> ERRONI

triangulatePoints(nearestRT[5], epcs_RT_real)
nPoints(nearestRT[5], epcs_RT_real , 5)
nPoints(nearestRT[5], epcs_RT_real , 10)
nPoints(nearestRT[5], epcs_RT_real , 15)
nPoints(nearestRT[5], epcs_RT_real , 30)

#matPlot2fig(scene,nearestRT[0])
