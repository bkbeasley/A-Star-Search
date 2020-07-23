import sys, pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (15, 242, 34)
RED = (252, 3, 3)
BLUE = (18, 235, 255)
WINDOW_WIDTH = 640
WINDOW_HEIGHT= 480
CELL_SIZE = 20

def main():
	global SCREEN, CLOCK, START_NODE_SET, END_NODE_SET 
	global START_NODE, END_NODE
	global MATRIX
	global OPEN_LIST, CLOSED_LIST
	global PATH_FOUND
	global PATH_NODES_X, PATH_NODES_Y

	pygame.init()
	SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	CLOCK = pygame.time.Clock()
	#SCREEN.fill(WHITE)

	START_NODE_SET = False
	START_NODE = {"x": None, "y": None, "f": None, "g": None, "h": None, "parent": None, "barrier": False}
	
	END_NODE = {"x": None, "y": None, "f": None, "g": None, "h": None, "parent": None, "barrier": False}
	END_NODE_SET = False

	OPEN_LIST = []
	CLOSED_LIST = []

	PATH_FOUND = False

	PATH_NODES_X = []
	PATH_NODES_Y = []

	drawCells()
	drawGrid()
	MATRIX = initCells()

	count = 0

	while True:

		#if (START_NODE_SET and END_NODE_SET):
		""" if START_NODE_SET and END_NODE_SET:
			if PATH_FOUND == False:
				runAlgorithm()
			else:
				count += 1
				if count == 1:
					showFinalPath()
					drawGrid() """

		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				# If space bar is pressed down
				if event.key == 32:
					if PATH_FOUND == False:
						runAlgorithm()
					else:
						count += 1
						if count <= 1:
							showFinalPath()
							drawGrid()

			#If the user clicks the left mouse button down
			if event.type == 5:
				if START_NODE_SET == False or END_NODE_SET == False:
					drawStartNode()
				else:
					drawBarrier()
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()


def drawGrid():
	for x in range(WINDOW_WIDTH):
		for y in range(WINDOW_HEIGHT):
			rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
			pygame.draw.rect(SCREEN, BLACK, rect, 1)

def drawCells():
	column = 0
	row = 0
	for x in range(WINDOW_WIDTH):
		for y in range(WINDOW_HEIGHT):
			rect = pygame.Rect(column, row, CELL_SIZE, CELL_SIZE)
			pygame.draw.rect(SCREEN, WHITE, rect)
			row += CELL_SIZE
		column += CELL_SIZE
		row = 0

def drawBarrier():
	# Find the column and row of the cell the user clicks on
	coordinates = pygame.mouse.get_pos()
	print("IN BARRIER: ", coordinates)

	if (coordinates[0] / CELL_SIZE) < 0:
		column = 0
	else:
		remainder = coordinates[0] % CELL_SIZE
		column = coordinates[0] - remainder
	

	remainder = coordinates[1] % CELL_SIZE
	row = coordinates[1] - remainder

	rect = pygame.Rect(column, row, CELL_SIZE, CELL_SIZE)
	
	pygame.draw.rect(SCREEN, BLUE, rect)

	x = int(column / CELL_SIZE)
	y = int(row / CELL_SIZE)

	MATRIX[x][y]['barrier'] = True
	print(MATRIX[x][y])



#def loadMatrix():
	#matrix = [[0 for row in range(int(WINDOW_HEIGHT / 20))] for col in range(int(WINDOW_WIDTH / 20))]
	#return matrix[0]

def findNeighbors(node):
	maxColSize = WINDOW_WIDTH / CELL_SIZE
	maxRowSize = WINDOW_HEIGHT / CELL_SIZE

	neighbors = []

	if (node["y"] + 1 < maxRowSize):
		x = node["x"]
		y = node["y"] + 1
		neighborSouth = MATRIX[x][y]
		neighbors.append(neighborSouth)

	if (node["y"] - 1 >= 0):
		x = node["x"]
		y = node["y"] - 1
		neighborNorth = MATRIX[x][y]
		neighbors.append(neighborNorth)

	if (node["x"] + 1 < maxColSize):
		x = node["x"] + 1
		y = node["y"] 
		neighborEast = MATRIX[x][y]
		neighbors.append(neighborEast)

	if (node["x"] - 1 >= 0):
		x = node["x"] - 1
		y = node["y"]
		neighborWest = MATRIX[x][y]
		neighbors.append(neighborWest)

	return neighbors

def initCells():
	matrix = [[{"x": col, "y": row, "f": None, "g": None, "h": None, "parent": None, "barrier": False} for row in range(int(WINDOW_HEIGHT / CELL_SIZE))] for col in range(int(WINDOW_WIDTH / CELL_SIZE))]
	return matrix

def calculateFCost(node):
	calculateGCost(node)
	calculateHCost(node)
	node["f"] = node["g"] + node["h"]

def calculateGCost(node):
	# Calculate the Manhattan distance from the Start Node
	distanceX = 0
	distanceY = 0

	distanceX = abs(node["x"] - START_NODE["x"])
	distanceY = abs(node["y"] - START_NODE["y"])
	node["g"] = distanceX + distanceY

def calculateHCost(node):
	# Calculate the Manhattan distance from the End Node
	distanceX = 0
	distanceY = 0

	distanceX = abs(node["x"] - END_NODE["x"])
	distanceY = abs(node["y"] - END_NODE["y"])
	node["h"] = distanceX + distanceY

def findLowestFCost():
	lowestVal = 0
	currentNode = {}

	for node in OPEN_LIST:
		if (node != START_NODE):
			lowestVal = node["f"]
			currentNode = node
			break

	for node in OPEN_LIST:
		if (node["f"] < lowestVal):
			lowestVal = node["f"]
			currentNode = node
	
	return currentNode

def setParentNode(neighborNode, currentNode):
	neighborNode["parent"] = {"x": currentNode["x"], "y": currentNode["y"]}

def runAlgorithm():
	global PATH_FOUND
	# Add start node to open
	OPEN_LIST.append(START_NODE)

	current = START_NODE

	calculateFCost(START_NODE)
	#setParentNode(START_NODE, START_NODE)

	count = 0

	while True:
		
		if (count > 0):
			current = findLowestFCost()
		
		#print("CURRENT NODE: ", current)
		#print("OPEN LIST BEFORE: ", OPEN_LIST)
		# Remove current from open list
		for node in OPEN_LIST:
			if node == current:
				OPEN_LIST.remove(node)

		#print("OPEN LIST AFTER: ", OPEN_LIST)
		# Add current to closed list
		CLOSED_LIST.append(current)

		#print("CLOSED LIST: ", CLOSED_LIST)
		# If the shortest path has been found

		if (current["x"] == END_NODE["x"] and current["y"] == END_NODE["y"]):
			#findPath()
			print("FINISHED!!!!!!!!!!")
			#print(current)
			displayPath(current)
			PATH_FOUND = True
			break
		
		# Get all of current's neighbors
		neighbors = findNeighbors(current)
		#print("NEIGHBORS: ", neighbors)

		for neighbor in neighbors:
			if (neighbor['barrier'] == True):
				continue

			if (isInClosedList(neighbor["x"], neighbor["y"]) == True):
				continue

			if (isInOpenList(neighbor["x"], neighbor["y"]) == False):
				calculateFCost(neighbor)
				setParentNode(neighbor, current)

			if (isInOpenList(neighbor["x"], neighbor["y"]) == False):
				OPEN_LIST.append(neighbor)
			#print("CURRENT NEIGHBOR: ", neighbor)
		count += 1

def displayOpenNodes():
	if not OPEN_LIST:
		return
	
	for node in OPEN_LIST:
		#print("NODE: ", node)
		rect = pygame.Rect(node["x"] * 20, node["y"] * 20, CELL_SIZE, CELL_SIZE)
		pygame.draw.rect(SCREEN, GREEN, rect)


def isInOpenList(x, y):
	for n in OPEN_LIST:
		if (n["x"] == x and n["y"] == y):
			return True

	return False

def isInClosedList(x, y):
	for n in CLOSED_LIST:
		if (n["x"] == x and n["y"] == y):
			return True
	
	return False

def showFinalPath():
	for x,y in zip(PATH_NODES_X, PATH_NODES_Y):
		if (x == START_NODE['x'] and y == START_NODE['y']):
			continue
		rect = pygame.Rect(x * 20, y * 20, CELL_SIZE, CELL_SIZE)
		pygame.draw.rect(SCREEN, RED, rect)
		

def displayPath(node):
	x = node["x"]
	y = node["y"]
	current = node
	while current['parent'] != None:
		#print("X: ", x, " Y: ", y)
		x = current['parent']['x']
		y = current['parent']['y']

		PATH_NODES_X.append(x)
		PATH_NODES_Y.append(y)

		current = MATRIX[x][y]

	#for n in node:
		#print(n['parent'][0]['parent'])
	""" for item in node:
		for key, value in item.items():
			if key == 'parent':
				print("AA: ", value['x']) """
				#rect = pygame.Rect(node["x"] * 20, node["y"] * 20, CELL_SIZE, CELL_SIZE)
				#pygame.draw.rect(SCREEN, RED, rect)
			


def drawStartNode():
	global START_NODE_SET, END_NODE_SET
	global START_NODE, END_NODE

	if START_NODE_SET == True and END_NODE_SET == True:
		return
	
	# Find the column and row of the cell the user clicks on
	coordinates = pygame.mouse.get_pos()

	if (coordinates[0] / CELL_SIZE) < 0:
		column = 0
	else:
		remainder = coordinates[0] % CELL_SIZE
		column = coordinates[0] - remainder
	

	remainder = coordinates[1] % CELL_SIZE
	row = coordinates[1] - remainder

	rect = pygame.Rect(column, row, CELL_SIZE, CELL_SIZE)
	
	pygame.draw.rect(SCREEN, BLACK, rect)

	if START_NODE_SET == False:
		START_NODE_SET = True
		START_NODE["x"] = int(column / CELL_SIZE)
		START_NODE["y"] = int(row / CELL_SIZE)
	elif END_NODE_SET == False:
		END_NODE_SET = True
		END_NODE["x"] = int(column / CELL_SIZE)
		END_NODE["y"] = int(row / CELL_SIZE)


if __name__ == "__main__":
	main()
