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
	with open('dades/dataTest.json','r') as f:
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
	"""
	"antenna_link","antenna_L1",0.15,0.17,0.03,0.5,-0.5,-0.5,-0.5
"antenna_link","antenna_L2",0.15,0.63,0.03,0.5,-0.5,-0.5,-0.5
"antenna_link","antenna_L3",0.15,1.1,0.03,0.5,-0.5,-0.5,-0.5
"antenna_link","antenna_L4",0.15,1.56,0.03,0.5,-0.5,-0.5,-0.5
"antenna_link","antenna_R1",0.15,0.17,0.14,0.5,0.5,0.5,-0.5
"antenna_link","antenna_R2",0.15,0.63,0.14,0.5,0.5,0.5,-0.5
"antenna_link","antenna_R3",0.15,1.1,0.14,0.5,0.5,0.5,-0.5
"antenna_link","antenna_R4",0.15,1.56,0.14,0.5,0.5,0.5,-0.5
	"""




print("Creating scene...")
size = 10
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


#print(type(relevantData[0]["robot_pose"]))




#print "Write data... \nFormat: posX,posY,dir \nExample: 33,70,top"
#x,y,dire = raw_input().split(",")
#print "Detection saved in position ("+str(x)+","+str(y)+") looking at " + dire + "."
