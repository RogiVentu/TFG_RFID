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
			'antena_port':d['ANTENNA_PORT'],
			'device_id':d['device_id']})

	return relData

def quatToDegrees():
	# antenas L = left antenas R = right


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






#print "Write data... \nFormat: posX,posY,dir \nExample: 33,70,top"
#x,y,dire = raw_input().split(",")
#print "Detection saved in position ("+str(x)+","+str(y)+") looking at " + dire + "."
