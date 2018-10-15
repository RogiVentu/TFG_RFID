
def createScene(size):
	scene = []
	for i in xrange(size):
		scene.append([])
	for i in xrange(size):
		for j in xrange(size):
			scene[i].append(j)
			scene[i][j] = 0
	return scene


print "Creating scene..."
size = 10
scene = createScene(size)
print "Scene " +str(size)+ "x" +str(size)+ " created"

print "Write data... \nFormat: posX,posY,dir \nExample: 33,70,top"


x,y,dire = raw_input().split(",")
print "Detection saved in position ("+str(x)+","+str(y)+") looking at " + dire + "."
