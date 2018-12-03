import json
import codecs
from pprint import pprint

def createScene(size):
	scene = []
	for i in xrange(size):
		scene.append([])
	for i in xrange(size):
		for j in xrange(size):
			scene[i].append(j)
			scene[i][j] = 0
	return scene

def readJSON():
	data = []
	with open('dades/dataTest_fakePos.json','r') as f:
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
		d["antenna_id"] = antList[d["device_id"] + "/" + d["antenna_port"]]

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

	for d in data:
		pos = d["robot_pose"][0]
		rot = d["robot_pose"][1]
		x = pos[0]
		y = pos[1]
		scene[x][y] = 1

	return scene

def printScene(scene, size):
	#this method should be remove for a plot library
	finalOut = ""
	for i in range(0,size):
		for j in range(0,size):
			finalOut += str(scene[i][j]) + "|"
		finalOut += "\n"
		for l in range(0, size*2-1):
			finalOut += "-"
		finalOut += "\n"

	return finalOut


print("Creating scene...")
size = 25
scene = createScene(size)
print("Scene " +str(size)+ "x" +str(size)+ " created")

print("Reading data...")
jsonData = readJSON()
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

print(relevantData)

print("Getting aproximated areas...")
sceneArea = getAreas(relevantData,scene)
print("Done")

print(printScene(sceneArea,size))


#print(type(relevantData[0]["robot_pose"]))




#print "Write data... \nFormat: posX,posY,dir \nExample: 33,70,top"
#x,y,dire = raw_input().split(",")
#print "Detection saved in position ("+str(x)+","+str(y)+") looking at " + dire + "."
